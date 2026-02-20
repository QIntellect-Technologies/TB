import os
import random
import time
import json
from typing import List, Dict, Optional
import concurrent.futures
from groq import Groq
from vector_store_faiss import FAISSVectorStore

class RAGEngine:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Initialize RAG engine with 4-key Groq rotation"""
        print("🔄 Initializing RAG Engine with Groq Multi-Key Rotation...")
        
        # Initialize FAISS vector store
        self.vector_store = FAISSVectorStore()
        
        # Performance Cache {query_hash: response}
        self.query_cache = {}
        self.cache_limit = 1000
        
        # Load PDF Page References
        self.pdf_references = self._load_pdf_references()

        self.llm_clients = []
        
        # Initialize 4 Groq Keys
        for i in range(1, 5):
            g_key = os.getenv(f"GROQ_API_KEY_{i}")
            if g_key:
                try:
                    self.llm_clients.append({
                        "name": f"Groq-{i}",
                        "client": Groq(api_key=g_key),
                        "model": "llama-3.3-70b-versatile",
                        "type": "groq"
                    })
                    print(f"✅ Groq-{i} initialized")
                except Exception as e: print(f"⚠️ Groq-{i} failed: {e}")

        self.use_llm = len(self.llm_clients) > 0
        if not self.use_llm:
            print("📝 No Groq providers available - using retrieval-only mode")
        else:
            print(f"🚀 Initializing parallel performance audit for {len(self.llm_clients)} keys...")
            self._parallel_performance_audit()
            print(f"⚡ RAG Engine ready. Fastest key: {self.llm_clients[0]['name']}")
    
    def _load_pdf_references(self) -> Dict:
        """Load PDF page reference mappings"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            pdf_ref_path = os.path.join(base_dir, 'dataset', 'TB_PDF_PAGE_REFERENCES.json')
            
            if os.path.exists(pdf_ref_path):
                with open(pdf_ref_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"📄 Loaded PDF references: {data['pdf_name']} ({data['total_pages']} pages)")
                    return data
            else:
                print("⚠️  PDF reference file not found")
                return None
        except Exception as e:
            print(f"⚠️  Failed to load PDF references: {e}")
            return None
    
    def _find_pdf_page_reference(self, query: str) -> Optional[str]:
        """Find matching PDF page for the query"""
        if not self.pdf_references:
            return None
        
        query_lower = query.lower()
        best_match = None
        max_keyword_matches = 0
        
        # Search through all pages
        for page_info in self.pdf_references.get('page_mappings', []):
            keyword_matches = 0
            
            # Count keyword matches
            for keyword in page_info.get('keywords', []):
                if keyword.lower() in query_lower:
                    keyword_matches += 1
            
            # Check if query matches any possible questions
            for question in page_info.get('possible_questions', []):
                if query_lower in question.lower() or question.lower() in query_lower:
                    keyword_matches += 3  # Boost for direct question match
            
            # Update best match if this page has more matches
            if keyword_matches > max_keyword_matches:
                max_keyword_matches = keyword_matches
                best_match = page_info
        
        # Return reference if we have a good match (at least 1 keyword)
        if best_match and max_keyword_matches >= 1:
            book_page = best_match.get('book_page', best_match.get('page', '?'))
            pdf_page = best_match.get('pdf_page', '?')
            pdf_name = self.pdf_references.get('pdf_name', 'TB Guide')
            
            # Build clickable PDF URL pointing to the specific page
            base_url = "https://tb-production-e244.up.railway.app"
            pdf_filename = "Childhood%20TB%20Training%20Desk%20Guide%20(2019)%20(1).pdf"
            pdf_url = f"{base_url}/static/pdfs/{pdf_filename}#page={pdf_page}"
            
            return f"\n\n� You can find more details on *Page {book_page}* of the _{pdf_name}_. Tap the link below to open it directly:\n🔗 {pdf_url}"
        
        return None

    
    def _parallel_performance_audit(self):
        """Ping all keys in parallel and rank by latency"""
        def check_latency(client_info):
            name = client_info["name"]
            client = client_info["client"]
            try:
                start = time.time()
                # Ultra-lightweight 1-token probe
                client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": "hi"}],
                    max_tokens=1
                )
                latency = time.time() - start
                client_info["latency"] = latency
                client_info["last_fail_time"] = 0
                return True
            except Exception as e:
                print(f"⚠️ Performance check failed for {name}: {e}")
                client_info["latency"] = 999.0 # Move to back of queue
                client_info["last_fail_time"] = time.time() # Mark as failed
                return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.llm_clients)) as executor:
            executor.map(check_latency, self.llm_clients)

        # Sort clients by latency (fastest first)
        self.llm_clients.sort(key=lambda x: x.get("latency", 999.0))
        
        print("\n⚡ Groq Performance Audit Results:")
        for client in self.llm_clients:
            lat = client.get("latency", 0)
            status = "FAST" if lat < 1.0 else "SLOW" if lat < 999 else "FAILED"
            print(f"📊 {client['name']} | Latency: {lat:.2f}s | Status: {status}")
        print("")

    
    def enhance_query_with_context(self, query: str, conversation_history: List[str], language: str = "English") -> str:
        """Enhance query with conversation context for better understanding"""
        query_lower = query.lower().strip()
        
        # GUARD RAIL 1: Profanity/Abuse Detection (Immediate Skip)
        profanity = ["fuck", "shit", "bitch", "asshole", "idiot", "stupid", "dumb", "hate", "dick", "bastard"]
        if any(bad in query_lower for bad in profanity):
            print(f"🛑 Skipping expansion for abuse query: '{query}'")
            return query

        # GUARD RAIL 2: Irrelevant/Personal Detection (Immediate Skip)
        irrelevant_keywords = ["love you", "miss you", "marry", "date", "kiss", "weather", "cricket", "football", "pizza", "laptop", "assignment"]
        if any(w in query_lower for w in irrelevant_keywords):
            print(f"🛑 Skipping expansion for irrelevant query: '{query}'")
            return query

        if not conversation_history or len(conversation_history) == 0:
            return query  # No context, return original query
        
        # KEY FIX: Don't expand if the subject is already clear (TB/Tuberculosis)
        # This prevents "Kidney TB" context poisoning for general questions
        if "tb" in query_lower or "tuberculosis" in query_lower or "تپ دق" in query_lower:
            return query
        
        # Extract topics from conversation history
        topics = self._extract_topics_from_history(conversation_history)
        
        # Handle pronouns and references
        pronouns = ["it", "that", "this", "them", "they", "its", "their"]
        has_pronoun = any(pronoun in query_lower.split() for pronoun in pronouns)
        
        # Handle follow-up questions
        follow_up_patterns = [
            "explain", "tell me more", "what about", "how about",
            "and", "also", "more details", "in detail", "elaborate"
        ]
        is_follow_up = any(pattern in query_lower for pattern in follow_up_patterns)
        
        # If query has pronouns or is a follow-up, add context
        if has_pronoun or is_follow_up or len(query.split()) < 5:
            if topics:
                # Add the most recent topic to the query
                main_topic = topics[0]
                enhanced = f"{main_topic} {query}"
                print(f"🔄 Enhanced query: '{query}' → '{enhanced}'")
                return enhanced
        
        return query
    
    def _extract_topics_from_history(self, history: List[str]) -> List[str]:
        """Extract main topics from conversation history, prioritizing recency"""
        topics = []
        
        # Medical keywords to look for
        medical_terms = [
            "mdr-tb", "xdr-tb", "multidrug-resistant", "extensively drug-resistant",
            "pulmonary", "extrapulmonary", "latent", "active", "spinal", "meningitis",
            "kidney", "brain", "bone", "joints", "bcg", "diagnosis", "symptoms"
        ]

        # Scan history from NEWEST to OLDEST
        for msg in reversed(history):
            msg_lower = msg.lower()
            # Find all mentioned terms in this specific message
            found_in_msg = [term for term in medical_terms if term in msg_lower]
            if found_in_msg:
                # Add found terms and stop if we have enough context
                for t in found_in_msg:
                    if t not in topics: topics.append(t)
                if len(topics) >= 1: return topics
        
        return topics
    
    def _detect_query_intent(self, query: str, language: str = "English") -> str:
        """Detect if user wants short answer, detailed explanation, or clinical reasoning"""
        query_lower = query.lower().strip()
        
        # Keywords that indicate a CLINICAL SCENARIO or MANAGEMENT question
        scenario_keywords_en = [
            "patient", "child exposed", "case", "scenario", "manage", "management",
            "what should be done", "what would you do", "how would you", "approach",
            "stopped medication", "missed dose", "contact", "exposed", "suspected",
            "risk", "risks", "what happens if", "consequences", "protocol",
            "steps", "guideline", "workup", "evaluate", "assessment"
        ]

        # Keywords that indicate user wants DETAILED explanation
        detail_keywords_en = [
            "explain", "describe", "tell me about", "elaborate", "in detail",
            "detailed", "comprehensive", "thoroughly", "extensively",
            "how does", "how do", "why does", "why do", "mechanism",
            "process", "step by step", "break down", "walk me through",
            "pathophysiology", "immunology", "pathogenesis", "role of"
        ]
        
        detail_keywords_ur = [
            "تفصیل", "وضاحت", "بتائیں", "سمجھائیں", "کیسے",
            "کیوں", "طریقہ", "مکمل", "تفصیلی"
        ]
        
        # Keywords that indicate user wants SHORT/BRIEF answer
        brief_keywords_en = [
            "what is", "what are", "define", "definition", "meaning",
            "briefly", "short", "quick", "simple", "in short",
            "summarize", "summary", "overview", "kya hai"
        ]
        
        brief_keywords_ur = [
            "کیا ہے", "کیا ہیں", "تعریف", "مطلب", "مختصر",
            "سادہ", "آسان", "فوری"
        ]
        
        # Check clinical scenario first (highest priority)
        if language == "English":
            if any(keyword in query_lower for keyword in scenario_keywords_en):
                return "clinical_scenario"
            if any(keyword in query_lower for keyword in detail_keywords_en):
                return "detailed"
            elif any(keyword in query_lower for keyword in brief_keywords_en):
                return "brief"
        else:  # Urdu
            if any(keyword in query for keyword in detail_keywords_ur):
                return "detailed"
            elif any(keyword in query for keyword in brief_keywords_ur):
                return "brief"
        
        # Default: if query is very short (< 5 words), assume brief
        word_count = len(query.split())
        if word_count <= 5:
            return "brief"
        else:
            return "detailed"
    
    def _preprocess_query(self, query: str, language: str) -> str:
        """Preprocess query - DISABLED expansion to let exact conversational Q&A work"""
        query = query.strip()
        
        # ❌ QUERY EXPANSION DISABLED
        # The expansion was sabotaging retrieval for conversational Q&A pairs.
        # Example: "Is TB contagious?" was expanded to "pulmonary Is TB contagious?"
        # which made RAG find wrong documents instead of the exact conversational Q&A.
        #
        # Now we let the RAG find exact matches from the conversational dataset.
        
        return query
    
    def _filter_results(self, results: List[Dict], query: str = "") -> List[Dict]:
        """Filter out form/document results, prioritize medical content"""
        if not results:
            return results
        
        # Check if user IS looking for forms
        seeking_forms = "form" in query.lower() or "tb0" in query.lower()
        
        # Filter out form-only results (TB01, TB05, etc.) unless requested
        filtered = []
        for result in results:
            answer = result.get('answer', '')
            category = result.get('category', '')
            question = result.get('question', '')
            
            # Skip if answer is form-related and user isn't asking for it
            if not seeking_forms:
                if answer.strip().startswith('TB0') or "Form" in category or "Documentation" in category:
                    continue
                if "TB0" in question and len(answer) < 50:
                    continue
            
            filtered.append(result)
        
        # If filtering removed everything, return original (fallback)
        if not filtered:
             # Try to return non-form items if possible, else return original
             non_forms = [r for r in results if not r.get('answer', '').startswith('TB0')]
             if non_forms: return non_forms
             return results
        
        return filtered
    
    def retrieve_context(self, query: str, language: str = "English", top_k: int = 10) -> List[Dict]:
        """Retrieve relevant context from vector store"""
        # Preprocess query
        expanded_query = self._preprocess_query(query, language)
        
        # Search with more results initially
        results = self.vector_store.search(expanded_query, language=language, top_k=top_k)
        
        # Filter out low-quality results
        filtered_results = self._filter_results(results, query=query)
        
        # Return top 5 after filtering
        return filtered_results[:5]
    
    def _synthesize_answer(self, query: str, context: List[Dict], language: str = "English") -> str:
        """Synthesize answer using LLM or fallback to rule-based extraction"""
        
        if not context or len(context) == 0:
            return "No relevant information found."
        
        # Try LLM synthesis first
        if self.use_llm:
            try:
                return self._llm_synthesize_groq(query, context, language)
            except Exception as e:
                print(f"⚠️  Groq LLM synthesis failed: {e}")
                # Fall through to fallback
        
        # Fallback: Simple extraction from top result
        best_answer = context[0].get('answer', '').strip()
        
        # Clean artifacts
        import re
        best_answer = re.sub(r'^\**Definition:?\**\s*', '', best_answer, flags=re.IGNORECASE)
        best_answer = re.sub(r'^\**Answer:?\**\s*', '', best_answer, flags=re.IGNORECASE)
        
        return best_answer
    
    def _call_llm_with_failover(self, prompt: str, system_instruction: str = None, temperature: float = 0.3, max_tokens: int = 500) -> str:
        """Call LLM providers with automatic failover and circuit breaker"""
        if not self.llm_clients:
            return None

        # Prepare messages
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        current_time = time.time()
        cooldown_period = 300 # 5 minutes

        for client_info in self.llm_clients:
            name = client_info["name"]
            
            # CIRCUIT BREAKER: Skip if failed recently
            last_fail = client_info.get("last_fail_time", 0)
            if current_time - last_fail < cooldown_period:
                print(f"⏩ Skipping {name} (Cooldown active)")
                continue

            client = client_info["client"]
            client_type = client_info["type"]
            model = client_info.get("model")

            try:
                print(f"🤖 Attempting with {name}...")
                
                if client_type == "groq" or client_type == "openai":
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout=3.0  # 🔥 Strict 3s timeout
                    )
                    return response.choices[0].message.content.strip()
                
                elif client_type == "cerebras":
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_completion_tokens=max_tokens
                    )
                    return response.choices[0].message.content.strip()
                
                elif client_type == "gemini":
                    # Gemini uses a different structure
                    gen_config = genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                    full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
                    response = client.generate_content(full_prompt, generation_config=gen_config)
                    return response.text.strip()

            except Exception as e:
                err_msg = str(e).lower()
                client_info["last_fail_time"] = time.time() # Trigger Circuit Breaker

                if "rate limit" in err_msg or "429" in err_msg or "too many requests" in err_msg:
                    print(f"⚠️ {name} Rate Limit reached. Switching to next provider...")
                else:
                    print(f"❌ {name} Error: {e}. Cooling down for 5 mins.")
                continue # Try next client

        print("🔥 All LLM providers failed or in cooldown.")
        return None

    def _llm_synthesize_groq(self, query: str, context: List[Dict], language: str) -> str:
        """Synthesize answer with clinical reasoning, depth, and scenario handling"""
        
        # Detect query intent
        intent = self._detect_query_intent(query, language)
        is_scared = any(w in query.lower() for w in ["scared", "diagnosed", "afraid", "worried", "preshan", "dar", "خوف", "پریشان"])
        
        # Adaptive token limits per intent
        if intent == "clinical_scenario":
            max_output_tokens = 900
        elif intent == "detailed":
            max_output_tokens = 800
        else:
            max_output_tokens = 200
        
        # Prepare context (top 5 documents for complex queries)
        top_k = 5 if intent in ["detailed", "clinical_scenario"] else 3
        context_text = "\n\n".join([
            f"Doc {i+1}: {doc.get('answer', '')}"
            for i, doc in enumerate(context[:top_k])
        ])
        
        if len(context_text) > 6000:
            context_text = context_text[:6000]
        
        if language == "English":
            system_instruction = (
                "You are a Senior TB Specialist and Clinical Educator with 20+ years of experience. "
                "You think like a clinician, not just an information retriever. "
                "For scenario-based questions: provide step-by-step clinical management. "
                "For 'explain' questions: provide in-depth pathophysiology including granuloma formation, "
                "Th1 immune response, IFN-gamma role, caseous necrosis, and latency mechanisms where relevant. "
                "For MDR-TB: include DST, GeneXpert, second-line drugs, isolation, and public health notification. "
                "Never repeat a symptom checklist when the question asks for management or clinical action. "
                "Format WhatsApp responses with *bold* for headers and bullet points for clarity."
            )

            if intent == "clinical_scenario":
                approach_instruction = (
                    "CLINICAL SCENARIO RULES:\n"
                    "- Identify the clinical problem clearly\n"
                    "- Provide a structured management plan with numbered steps\n"
                    "- Include investigations (Mantoux, IGRA, GeneXpert, CXR, sputum smear etc.) where relevant\n"
                    "- Include treatment options (IPT, standard regimen, second-line etc.) where relevant\n"
                    "- Mention risks, drug resistance concerns, and public health aspects if applicable\n"
                    "- DO NOT list generic TB symptoms — answer the management question directly"
                )
            elif intent == "detailed":
                approach_instruction = (
                    "DETAILED EXPLANATION RULES:\n"
                    "- Provide a thorough, multi-paragraph explanation\n"
                    "- Include mechanism, pathophysiology, or immunology as relevant\n"
                    "- For immune response: cover Th1, macrophage activation, IFN-gamma, granuloma, TNF-alpha, latency\n"
                    "- For MDR-TB management: cover DST, GeneXpert, second-line drugs, isolation protocols\n"
                    "- Use medical terminology with brief explanations for clarity"
                )
            else:
                approach_instruction = (
                    "BRIEF ANSWER RULES:\n"
                    "- Answer in 1-3 sentences maximum\n"
                    "- Be direct, medically accurate, and clear"
                )

            empathy_note = "Begin with brief reassurance: 'With proper treatment, most people fully recover.' before the clinical answer." if is_scared else ""

            prompt = f"""MEDICAL KNOWLEDGE BASE:
{context_text}

CLINICAL QUESTION: {query}

{approach_instruction}
{empathy_note}

ADDITIONAL RULES:
- Never suggest MDR-TB drugs (BPaL, BPaLM, Linezolid) unless MDR is explicitly mentioned
- For general TB, refer to 'standard 6-month HRZE/HR regimen'
- Cite specific investigations and management steps for clinical scenarios
- Format clearly for WhatsApp using *bold* headers and bullet points
"""
        else:  # Urdu
            system_instruction = (
                "آپ ٹی بی کے سینئر طبی ماہر اور کلینیکل معلم ہیں۔ "
                "کلینیکل سیناریو سوالوں کے لیے قدم بہ قدم انتظام فراہم کریں۔ "
                "تفصیلی سوالوں کے لیے گہری pathophysiology بیان کریں۔ "
                "WhatsApp فارمیٹ: *بولڈ* ہیڈرز اور بلٹ پوائنٹس استعمال کریں۔"
            )

            if intent == "clinical_scenario":
                approach_instruction = "یہ ایک کلینیکل کیس ہے۔ قدم بہ قدم انتظامی منصوبہ دیں، جانچ اور علاج شامل کریں۔"
            elif intent == "detailed":
                approach_instruction = "تفصیلی وضاحت دیں، بشمول میکانزم، pathophysiology اور طبی پہلو۔"
            else:
                approach_instruction = "صرف 1-2 مختصر جملوں میں جواب دیں۔"

            prompt = f"""طبی معلومات:
{context_text}

سوال: {query}

ہدایت: {approach_instruction}
علاج: صرف اس وقت MDR ادویات کا ذکر کریں جب صارف MDR کا ذکر کرے۔
"""

        result = self._call_llm_with_failover(prompt, system_instruction=system_instruction, max_tokens=max_output_tokens, temperature=0.4)
        return result if result else self._synthesize_answer(query, context, language)
    
    def build_prompt(self, query: str, context: List[Dict], language: str = "English") -> str:
        """Build prompt for LLM with retrieved context"""
        if language == "English":
            prompt = f"""You are a TB (Tuberculosis) medical expert. Answer the following question accurately using ONLY the provided context.

Question: {query}

Context (from TB Expert Database):
"""
            for i, ctx in enumerate(context, 1):
                prompt += f"\n{i}. [{ctx['category']}]\n"
                prompt += f"   Q: {ctx['question']}\n"
                prompt += f"   A: {ctx['answer']}\n"
            
            prompt += """\nInstructions:
- Provide a clear, accurate answer based on the context above
- If the context doesn't contain enough information, say so
- Use medical terminology appropriately
- Keep the answer concise and professional
- Cite which context number(s) you used

Answer:"""
        
        else:  # Urdu
            prompt = f"""آپ ٹی بی (تپِ دق) کے طبی ماہر ہیں۔ صرف فراہم کردہ معلومات کی بنیاد پر درست جواب دیں۔

سوال: {query}

معلومات (ٹی بی ایکسپرٹ ڈیٹابیس سے):
"""
            for i, ctx in enumerate(context, 1):
                prompt += f"\n{i}. [{ctx['category']}]\n"
                prompt += f"   سوال: {ctx['question']}\n"
                prompt += f"   جواب: {ctx['answer']}\n"
            
            prompt += """\nہدایات:
- اوپر دی گئی معلومات کی بنیاد پر واضح اور درست جواب دیں
- اگر کافی معلومات نہیں ہیں تو بتائیں
- طبی اصطلاحات مناسب طریقے سے استعمال کریں
- جواب مختصر اور پیشہ ورانہ رکھیں

جواب:"""
        
        return prompt
    
    def generate_answer(self, query: str, language: str = "English", original_query: str = None, conversation_history: List[str] = None) -> Dict:
        """Full RAG Pipeline: Context + LLM Synthesis with Cache"""
        # 1. Check Cache
        cache_key = f"{language}:{query.lower().strip()}"
        if cache_key in self.query_cache:
            print(f"⚡ Cache Hit for '{query[:30]}...'")
            return self.query_cache[cache_key]

        # --- PHASE 0: AUTO-LANGUAGE DETECTION (If not provided or default) ---
        import re
        urdu_pattern = re.compile(r'[\u0600-\u06FF]')
        if urdu_pattern.search(query):
            language = "Urdu"
        
        start_time = time.time()
        check_query = original_query if original_query else query
        
        # --- PHASE 1: CHECK IF USER IS RESPONDING TO SYMPTOM QUESTION ---
        if conversation_history:
            symptom_response = self._check_symptom_response(check_query, conversation_history, language)
            if symptom_response:
                return symptom_response
        
        # --- PHASE 2: INTENT CLASSIFICATION ---
        intent_category = self._classify_chat_intent(check_query, language)
        
        # --- PHASE 3: HANDLE TB SYMPTOMS QUERY (SPECIAL CASE) ---
        if self._is_symptom_query(check_query):
            symptom_response = self._get_formatted_symptoms(language)
            result = {
                "answer": symptom_response,
                "sources": [],
                "method": "symptom_template",
                "category": "Symptoms"
            }
            self.query_cache[cache_key] = result
            return result
        
        # --- PHASE 4: HANDLE NON-MEDICAL CHAT ---
        if intent_category in ["greeting", "small_talk", "irrelevant", "abuse"]:
            if self.use_llm:
                try:
                    chat_reply = self._llm_conversational_reply(check_query, intent_category, language)
                    result = {
                        "answer": chat_reply,
                        "sources": [],
                        "method": "llm_chat",
                        "category": "Chat"
                    }
                    self.query_cache[cache_key] = result
                    return result
                except: pass
            
            # Static Fallback
            result = {
                "answer": "I am a TB specialist. How can I help with symptoms or treatment?" if language == "English" else "میں ٹی بی کا ماہر ہوں۔ میں علامات یا علاج میں کیسے مدد کر سکتا ہوں؟",
                "sources": [], 
                "method": "intent_fallback"
            }
            self.query_cache[cache_key] = result
            return result

        # --- PHASE 5: MEDICAL RAG ---
        context = self.retrieve_context(query, language=language, top_k=10)
        
        if not context:
            return {"answer": "No relevant info found.", "sources": [], "method": "no_results"}
        
        # Synthesize
        final_result = None
        if self.use_llm:
            try:
                synthesized = self._llm_synthesize_groq(query, context, language)
                final_result = {
                    "answer": synthesized,
                    "sources": context[:3],
                    "method": "LLM",
                    "latency": round(time.time() - start_time, 3)
                }
            except Exception as e:
                print(f"⚠️ LLM fail: {e}")
        
        if not final_result:
            answer = self._synthesize_answer(query, context, language)
            final_result = {
                "answer": answer,
                "sources": context[:3],
                "method": "Retrieval",
                "latency": round(time.time() - start_time, 3)
            }
        
        # 🔥 APPEND PDF PAGE REFERENCE (if found)
        pdf_ref = self._find_pdf_page_reference(check_query)
        if pdf_ref:
            final_result["answer"] += pdf_ref
        
        # Update Cache
        if len(self.query_cache) < self.cache_limit:
            self.query_cache[cache_key] = final_result
            
        return final_result

    def _classify_chat_intent(self, query: str, language: str) -> str:
        """Classify query into Greeting, Medical, Irrelevant, etc."""
        q_lower = query.lower().strip()
        
        # 1. CRITICAL: Abuse/Profanity Check (TOP PRIORITY)
        profanity = ["fuck", "shit", "bitch", "asshole", "idiot", "stupid", "dumb", "hate", "dick", "bastard", "fool"]
        if any(bad in q_lower for bad in profanity):
            return "abuse"
            
        # 2. Irrelevant / Personal / Off-topic
        irrelevant = [
            "love you", "miss you", "marry", "kiss", "date", 
            "python", "java", "code", "programming", "weather", "football", 
            "cricket", "politics", "pizza", "laptop", "assignment", "song", "movie"
        ]
        if any(w in q_lower for w in irrelevant):
            return "irrelevant"

        # 3. Greetings & Starters
        greetings = ["hi", "hello", "hey", "salam", "assalam", "good morning", 
                     "listen", "excuse me", "?", "start", "yo", "listen"]
        if q_lower in greetings or q_lower.replace("?","").strip() in greetings:
            return "greeting"
            
        # 4. Small Talk / Persona / Identity
        identity_phrases = ["who are you", "who r u", "who i am", "who am i", "your name", "what are you", "what can you do", "help me with"]
        if any(phrase in q_lower for phrase in identity_phrases):
            return "small_talk"
            
        small_talk = ["how are you", "how r u", "how are u", "doing well", "good to see"]
        if any(phrase in q_lower for phrase in small_talk):
            return "small_talk"

        # 5. Check for MEDICAL keywords
        medical_keywords = [
            "tb", "tuberculosis", "cough", "blood", "fever", "sweate", "weight", 
            "treatment", "medicine", "drug", "symptom", "pain", "doctor", "cure", "curable", "recover",
            "hospital", "test", "x-ray", "mantoux", "vaccine", "bcg",
            "rifampicin", "isoniazid", "ethambutol", "pyrazinamide",
            "تپ دق", "کھانسی", "بخار", "علاج", "دوائی", "صحت", "شفاء"
        ]
        if any(w in q_lower for w in medical_keywords):
            return "medical"
            
        # Default to medical (let RAG try, it will likely return fallback)
        return "medical"

    def _check_symptom_response(self, query: str, conversation_history: List[str], language: str) -> Optional[Dict]:
        """Check if user is responding to the symptom question"""
        if not conversation_history:
            return None
        
        # Check if symptom template was shown recently (last 2 messages)
        recent_history = conversation_history[-2:]
        symptom_template_shown = any("Tell me, from all of these which symptoms" in msg or 
                                     "مجھے بتائیں ان میں سے کون سی علامات" in msg 
                                     for msg in recent_history)
        
        if not symptom_template_shown:
            return None
        
        # User is responding to symptoms - analyze their response
        q_lower = query.lower().strip()
        
        # Define all TB symptoms to detect
        all_symptoms = {
            "cough": {"severity": "common", "category": "Chest", 
                     "advice": "Persistent cough for more than 2 weeks is a key TB symptom. You should get tested immediately with a sputum test and chest X-ray."},
            "fever": {"severity": "common", "category": "Systemic",
                     "advice": "Low-grade fever persisting for more than 2 weeks is concerning for TB. Please consult a doctor for proper evaluation and testing."},
            "headache": {"severity": "serious", "category": "Meningitis",
                        "advice": "Headache can be a sign of TB meningitis, especially if accompanied by neck stiffness, vomiting, or confusion. This is a medical emergency - seek immediate medical attention."},
            "night sweat": {"severity": "common", "category": "Systemic",
                           "advice": "Night sweats combined with other symptoms like fever and weight loss are classic signs of TB. Please get tested soon."},
            "weight loss": {"severity": "common", "category": "Systemic",
                           "advice": "Unexplained weight loss and failure to gain weight despite diet are concerning. Combined with other symptoms, this requires TB screening."},
            "shortness of breath": {"severity": "moderate", "category": "Chest",
                                   "advice": "Difficulty breathing suggests lung involvement. This needs immediate medical evaluation and chest X-ray."},
            "chest pain": {"severity": "moderate", "category": "Chest",
                          "advice": "Chest pain with cough may indicate lung infection. Please see a doctor for proper diagnosis."},
            "back pain": {"severity": "moderate", "category": "Bones/Spine",
                         "advice": "Persistent back pain could indicate spinal TB (Pott's disease). You need an X-ray or MRI and medical consultation."},
            "vomiting": {"severity": "serious", "category": "Meningitis",
                        "advice": "Vomiting combined with headache and neck stiffness may indicate TB meningitis - seek emergency medical care."},
            "diarrhea": {"severity": "moderate", "category": "Abdomen",
                        "advice": "Chronic diarrhea with abdominal distension may suggest abdominal TB. Medical evaluation is needed."},
            "joint swelling": {"severity": "moderate", "category": "Joints",
                              "advice": "Joint swelling with slow onset can be TB arthritis. Consult a doctor for joint examination and testing."}
        }
        
        # Urdu symptom words mapping
        urdu_symptoms = {
            "کھانسی": "cough",
            "بخار": "fever",
            "سر درد": "headache",
            "پسینہ": "night sweat",
            "وزن": "weight loss",
            "سانس": "shortness of breath"
        }
        
        # Detect mentioned symptoms
        detected_symptoms = []
        
        for symptom_key, symptom_data in all_symptoms.items():
            if symptom_key.replace(" ", "") in q_lower.replace(" ", ""):
                detected_symptoms.append((symptom_key, symptom_data))
        
        # Check Urdu symptoms
        for urdu_word, eng_symptom in urdu_symptoms.items():
            if urdu_word in query:
                if eng_symptom in all_symptoms:
                    detected_symptoms.append((eng_symptom, all_symptoms[eng_symptom]))
        
        if detected_symptoms:
            # Generate personalized response
            response = self._generate_symptom_advice(detected_symptoms, language)
            return {
                "answer": response,
                "sources": [],
                "method": "symptom_followup",
                "category": "Symptom Analysis"
            }
        
        # If no specific symptom detected but user mentioned "i have" or "i got"
        if any(phrase in q_lower for phrase in ["i have", "i got", "i'm having", "میں نے", "مجھے"]):
            advice = """I understand you're experiencing symptoms. To help you better, please:

1. **Visit a doctor immediately** for proper diagnosis
2. **Get tested** - Sputum test, chest X-ray, and Mantoux test
3. **Don't delay** - Early diagnosis is crucial for TB treatment

Which other symptoms from the list are you experiencing?""" if language == "English" else """میں سمجھتا ہوں کہ آپ علامات کا سامنا کر رہے ہیں۔ آپ کی بہتر مدد کے لیے:

1. **فوری طور پر ڈاکٹر سے ملیں** مناسب تشخیص کے لیے
2. **ٹیسٹ کروائیں** - بلغم کا ٹیسٹ، سینے کا ایکسرے، اور مینٹوکس ٹیسٹ
3. **تاخیر نہ کریں** - ٹی بی کے علاج کے لیے جلد تشخیص بہت ضروری ہے

فہرست میں سے آپ کو اور کون سی علامات ہیں؟"""
            
            return {
                "answer": advice,
                "sources": [],
                "method": "symptom_followup",
                "category": "General Advice"
            }
        
        return None
    
    def _generate_symptom_advice(self, symptoms: List[tuple], language: str) -> str:
        """Generate personalized advice based on detected symptoms"""
        if language == "Urdu":
            intro = "**آپ کی علامات کی بنیاد پر:**\n\n"
        else:
            intro = "**Based on your symptoms:**\n\n"
        
        advice_text = intro
        
        # Add specific advice for each symptom
        for symptom_name, symptom_data in symptoms:
            if language == "English":
                advice_text += f"• **{symptom_name.title()}** ({symptom_data['category']}): {symptom_data['advice']}\n\n"
            else:
                # Simplified Urdu response
                advice_text += f"• **{symptom_name.title()}**: فوری طور پر ڈاکٹر سے ملیں اور ٹیسٹ کروائیں۔\n\n"
        
        # Add urgent action recommendation
        severity_levels = [s[1]['severity'] for s in symptoms]
        
        if "serious" in severity_levels:
            if language == "English":
                advice_text += "⚠️ **URGENT**: Your symptoms suggest a serious condition. Please seek **immediate medical attention** at the nearest hospital.\n\n"
            else:
                advice_text += "⚠️ **فوری**: آپ کی علامات سنگین حالت کی نشاندہی کرتی ہیں۔ براہ کرم قریبی ہسپتال میں **فوری طبی امداد** حاصل کریں۔\n\n"
        
        # Follow-up questions
        if language == "English":
            advice_text += "**Next Steps:**\n"
            advice_text += "1. How long have you had these symptoms?\n"
            advice_text += "2. Do you have any other symptoms from the list?\n"
            advice_text += "3. Have you been in contact with anyone diagnosed with TB?"
        else:
            advice_text += "**اگلے قدم:**\n"
            advice_text += "1. آپ کو یہ علامات کتنے عرصے سے ہیں؟\n"
            advice_text += "2. کیا آپ کو فہرست میں سے کوئی اور علامات ہیں؟\n"
            advice_text += "3. کیا آپ ٹی بی سے متاثرہ کسی شخص کے رابطے میں رہے ہیں؟"
        
        return advice_text
    
    def _is_symptom_query(self, query: str) -> bool:
        """Detect if user is asking about TB symptoms (not clinical scenarios or management)"""
        q_lower = query.lower().strip()
        
        # CRITICAL: Clinical scenario/management queries must NOT trigger symptom template
        scenario_override = [
            "patient", "child exposed", "exposed", "stopped", "missed dose",
            "what should", "how would", "manage", "management", "approach",
            "risk", "risks", "consequences", "contact", "suspected",
            "case", "scenario", "protocol", "steps", "workup"
        ]
        if any(word in q_lower for word in scenario_override):
            return False

        # Exclude queries asking about types, causes, treatment, etc.
        exclude_keywords = [
            "type", "types", "kind", "kinds", "category", "categories",
            "cause", "causes", "treatment", "cure", "medicine", "drug",
            "test", "diagnosis", "prevent", "vaccination"
        ]
        if any(word in q_lower for word in exclude_keywords):
            return False
        
        # English symptom keywords - must be explicit
        symptom_keywords = [
            "symptom", "symptoms", "sign", "signs",
            "indication", "indications"
        ]
        
        # Urdu symptom keywords
        urdu_symptom_keywords = [
            "علامات", "علامت", "نشانیاں", "نشانی"
        ]
        
        # Check for TB + symptom combination
        has_tb = any(word in q_lower for word in ["tb", "tuberculosis", "تپ دق"])
        has_symptom = any(word in q_lower for word in symptom_keywords + urdu_symptom_keywords)
        
        return has_tb and has_symptom
    
    def _get_formatted_symptoms(self, language: str = "English") -> str:
        """Return formatted TB symptoms with follow-up question"""
        
        if language == "Urdu":
            # Urdu version
            return """**ٹی بی کی علامات:**

**سینہ:**
• کھانسی > 2 ہفتے (مسلسل اور بہتر نہیں ہو رہی)
• بلغم
• سانس میں تکلیف
• یک طرفہ گھرگھراہٹ، پھیکا پن

**عمومی:**
• بخار > 2 ہفتے، ہلکا (99°F)
• رات کو پسینہ آنا
• غذائی کمی یا وزن میں اضافہ نہ ہونا
• کمزور قوت مدافعت: کالی کھانسی یا خسرہ کی تاریخ (گزشتہ 6 ماہ میں)
• لمف نوڈز: گردن کے لمف نوڈز (بڑھے ہوئے، بغیر درد، جمع یا پھوڑا)
• BCG کا نشان نہیں

**دماغی بخار:**
• سر درد، الٹی، چڑچڑاپن، سستی
• گردن میں اکڑن، ابھرا ہوا پیشانی کا حصہ، بے ہوشی

**پیٹ:**
• دائمی اسہال، پھولا ہوا پیٹ، کوئی گانٹھ، یا پیٹ میں پانی
**ہڈیاں اور جوڑ:**
• کمر درد، اکڑن، گانٹھ، خرابی، لنگڑانا
• جوڑ کی یک طرفہ سوجن، کوئی نرمی (آہستہ شروعات)

مجھے بتائیں ان میں سے کون سی علامات آپ کو ہیں؟"""
        
        else:
            # English version
            return """**TB Symptoms:**

**Chest:**
• Cough > 2 weeks (unremitting and not improving)
• Sputum
• Shortness of breath
• Unilateral wheeze, dullness

**Systemic:**
• Fever > 2 weeks, low grade (99°F)
• Sweating at night
• Malnutrition or failure to gain weight (Protein Caloric Malnutrition — Grade 3), has not responded to 1 month dietary plan
• Low immune status: H/O pertussis or measles (in last 6 months)
• Lymph nodes: Cervical lymph nodes (enlarged, painless, matted, or there is an abscess with or without discharge)
• BCG scar absent

**Meningitis:**
• Headache, vomiting, irritability, lethargic
• Neck stiffness, bulging anterior fontanella, coma

**Abdomen:**
• Chronic diarrhea, distended abdomen, any mass, or ascites

**Bones and Joints:**
• Backache, stiffness, lump, deformity, limp
• Unilateral swelling of joint, any tenderness (slow onset)

Tell me, from all of these which symptoms do you have?"""
    
    def _llm_conversational_reply(self, query: str, intent: str, language: str) -> str:
        """Generate human-like, professional reply for non-medical interactions"""
        
        system_instruction = ""
        
        if intent == "greeting":
            system_instruction = "Senior TB Medical Specialist Assistant. Greeting only. Exactly 1 short sentence."
        elif intent == "small_talk":
            system_instruction = "Senior TB Medical Specialist Assistant. Identity: You are the Senior TB Medical Specialist Assistant. Exactly 1 short sentence. No personal life talk."
        elif intent == "abuse":
            system_instruction = "Senior TB Medical Specialist Assistant. User offensive. 1 sentence: state you handle medical queries only."
        else: # irrelevant
            system_instruction = "Senior TB Medical Specialist Assistant. Identity: Senior TB Medical Specialist Assistant. Refuse non-TB topic politely. 1 sentence only."
            
        if language != "English":
            system_instruction += " Reply in Urdu."

        result = self._call_llm_with_failover(query, system_instruction=system_instruction, temperature=0.3, max_tokens=60)
        
        if result:
            return result
            
        # Hard Fallback
        return "I am a Tuberculosis (TB) specialist. I can only assist with questions related to TB symptoms, treatment, and protocols."


    def _merge_similar_content(self, content_list: List[str]) -> List[str]:
        """Remove duplicate/very similar content"""
        unique = []
        seen_keywords = set()
        
        for content in content_list:
            # Extract key words (first 50 chars)
            key = content[:50].lower()
            
            # Check if we've seen very similar content
            is_duplicate = False
            for seen_key in seen_keywords:
                # Simple similarity check
                if key in seen_key or seen_key in key:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(content)
                seen_keywords.add(key)
        
        return unique


if __name__ == "__main__":
    # Test RAG engine
    print("\n" + "="*60)
    print("🧪 TESTING RAG ENGINE")
    print("="*60)
    
    # Initialize (without LLM for now)
    rag = RAGEngine()
    
    # Test queries
    test_queries = [
        ("What are the main symptoms of tuberculosis?", "English"),
        ("How is MDR-TB different from regular TB?", "English"),
        ("ٹی بی کی علامات کیا ہیں؟", "Urdu")
    ]
    
    for query, lang in test_queries:
        print(f"\n{'='*60}")
        print(f"Query ({lang}): {query}")
        print("-"*60)
        
        result = rag.generate_answer(query, language=lang)
        
        print(f"Method: {result['method']}")
        print(f"\nAnswer:\n{result['answer'][:300]}...")
        
        if result.get('sources'):
            print(f"\nSources ({len(result['sources'])}):")
            for i, src in enumerate(result['sources'][:2], 1):
                print(f"  {i}. [{src['category']}] Score: {src['relevance_score']:.3f}")
