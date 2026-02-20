import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tb_knowledge_base import get_knowledge_base

# Page configuration
st.set_page_config(
    page_title="TB Healthcare Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        background-color: #E3F2FD;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FFA726;
        background-color: #FFF3E0;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #66BB6A;
        background-color: #E8F5E9;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_and_knowledge():
    """Load the sentence transformer model and prepare knowledge base"""
    # Load model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Get knowledge
    knowledge = get_knowledge_base()
    
    # Split knowledge into sections
    sections = knowledge.split('\n## ')
    sections = ['## ' + section.strip() for section in sections if section.strip()]
    sections[0] = sections[0].replace('## ', '')  # Remove from first section
    
    # Create embeddings for all sections
    section_embeddings = model.encode(sections)
    
    return model, sections, section_embeddings

def get_relevant_info(query, model, sections, section_embeddings, top_k=3):
    """Get relevant information based on query"""
    # Encode the query
    query_embedding = model.encode([query])
    
    # Calculate similarities
    similarities = cosine_similarity(query_embedding, section_embeddings)[0]
    
    # Get top k most similar sections
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Return relevant sections
    relevant_sections = [sections[i] for i in top_indices if similarities[i] > 0.2]
    
    return relevant_sections if relevant_sections else [sections[0]]

def format_response(relevant_info):
    """Format the response nicely"""
    response = "Based on the TB medical knowledge, here's what I found:\n\n"
    response += "\n\n".join(relevant_info)
    response += "\n\n---\n\n**📌 Important Note:** This information is for educational purposes only. For personalized medical advice, diagnosis, or treatment, please consult a qualified healthcare professional."
    return response

def main():
    # Header
    st.markdown('<div class="main-header">🩺 TB Healthcare Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI-powered guide for Tuberculosis information</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("📚 About TB Bot")
        st.write("""
        This intelligent chatbot provides comprehensive, evidence-based information about Tuberculosis (TB):
        
        ✅ **Symptoms & Diagnosis**  
        ✅ **Types of TB**  
        ✅ **Treatment Options**  
        ✅ **Prevention Methods**  
        ✅ **Nutrition & Lifestyle**  
        ✅ **Myths vs Facts**
        """)
        
        st.markdown("---")
        st.markdown("### 🌐 Quick Links")
        st.markdown("- [WHO TB Information](https://www.who.int/health-topics/tuberculosis)")
        st.markdown("- [NIKSHAY Portal (India)](https://nikshay.in/)")
        st.markdown("- [CDC TB Guide](https://www.cdc.gov/tb/)")
        
        st.markdown("---")
        st.markdown("### 📞 Helplines")
        st.success("""
        **India TB Helpline**  
        📞 1800-11-6666
        
        **WHO Global**  
        📞 +41 22 791 21 11
        """)
        
        st.markdown("---")
        st.warning("⚠️ **Disclaimer:** This chatbot provides general information only. Always consult healthcare professionals for medical advice.")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Ask Your TB-Related Questions")
        
        # Initialize model and knowledge
        with st.spinner("🔄 Loading AI model and TB knowledge base..."):
            model, sections, section_embeddings = load_model_and_knowledge()
        
        # Initialize session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            # Add welcome message
            welcome_msg = """
            👋 Welcome! I'm your TB Healthcare Assistant. I can help you with:
            
            - Understanding TB symptoms and diagnosis
            - Information about TB types (Active vs Latent)
            - Treatment options and DOTS program
            - Prevention strategies
            - Nutrition and lifestyle guidance
            - Myths vs facts about TB
            
            Feel free to ask me anything about Tuberculosis!
            """
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("💭 Ask me anything about Tuberculosis..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Searching TB knowledge base..."):
                    relevant_info = get_relevant_info(prompt, model, sections, section_embeddings)
                    response = format_response(relevant_info)
                    st.markdown(response)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Quick action buttons
        st.markdown("---")
        st.markdown("#### 🔍 Quick Questions (Click to ask)")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("❓ What are TB symptoms?"):
                st.session_state.messages.append({"role": "user", "content": "What are the main symptoms of tuberculosis?"})
                st.rerun()
        
        with col_b:
            if st.button("💊 How is TB treated?"):
                st.session_state.messages.append({"role": "user", "content": "How is tuberculosis treated? Tell me about the DOTS program."})
                st.rerun()
        
        with col_c:
            if st.button("🛡️ How to prevent TB?"):
                st.session_state.messages.append({"role": "user", "content": "How can I prevent tuberculosis? What precautions should I take?"})
                st.rerun()
        
        col_d, col_e, col_f = st.columns(3)
        
        with col_d:
            if st.button("🍎 TB nutrition guide"):
                st.session_state.messages.append({"role": "user", "content": "What foods should TB patients eat? Give me nutrition advice."})
                st.rerun()
        
        with col_e:
            if st.button("🔬 TB diagnosis methods"):
                st.session_state.messages.append({"role": "user", "content": "How is TB diagnosed? What tests are used?"})
                st.rerun()
        
        with col_f:
            if st.button("📖 Active vs Latent TB"):
                st.session_state.messages.append({"role": "user", "content": "What is the difference between active TB and latent TB?"})
                st.rerun()
    
    with col2:
        st.markdown("### 📊 TB Quick Facts")
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**🦠 What is TB?**")
        st.write("Bacterial disease caused by *Mycobacterium tuberculosis*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("**✅ Curability**")
        st.write("**95%+ cure rate** with proper 6-9 month treatment")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**📡 Transmission**")
        st.write("Spreads through air when infected person coughs/sneezes")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**⚠️ See a Doctor If:**")
        st.write("""
        - Cough lasting > 3 weeks
        - Blood in cough/sputum
        - Night sweats > 2 weeks
        - Unexplained weight loss
        - Persistent fever
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🌍 Global Impact")
        st.metric("Annual TB Cases", "10.6M", help="Global TB cases in 2022")
        st.metric("TB Deaths", "1.3M", help="Annual TB deaths worldwide")
        st.metric("India's Burden", "27%", help="India accounts for 27% of global TB cases")
        
        st.markdown("---")
        st.markdown("### 🛠️ Chat Controls")
        if st.button("🔄 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📥 Download TB Info", use_container_width=True):
            st.download_button(
                label="📄 Download Full TB Guide",
                data=get_knowledge_base(),
                file_name="tb_complete_guide.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
