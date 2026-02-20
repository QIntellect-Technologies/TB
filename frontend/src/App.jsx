import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Activity, User, Bot, Trash2, ShieldCheck, Info, Image, AlertCircle, CheckCircle2 } from 'lucide-react';

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { id: 1, text: "Welcome to TB Expert Global. How can I assist you with clinical protocols, drugs, or symptoms today?", sender: 'bot', lang: 'English' }
  ]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [ragMode, setRagMode] = useState(false); // RAG toggle
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchStats();
    scrollToBottom();
  }, [messages]);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/stats`);
      setStats(res.data);
    } catch (err) { console.error("Stats fail"); }
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const isUrdu = (text) => /[\u0600-\u06FF]/.test(text);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { id: Date.now(), text: input, sender: 'user', lang: isUrdu(input) ? 'Urdu' : 'English' };
    setMessages(prev => [...prev, userMsg]);
    const currentInput = input;
    setInput("");
    setLoading(true);

    try {
      // Use RAG endpoint if enabled, otherwise use standard chat
      const endpoint = ragMode ? `${API_BASE}/chat-rag` : `${API_BASE}/chat`;
      const res = await axios.post(endpoint, { message: currentInput });

      const botMsg = {
        id: Date.now() + 1,
        text: res.data.reply,
        sender: 'bot',
        lang: res.data.language,
        category: res.data.category,
        method: res.data.method,
        sources: res.data.sources // RAG sources if available
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { id: Date.now() + 1, text: "Connection Error. Is the backend running?", sender: 'bot', lang: 'English' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleXrayUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    // Add a placeholder message for the upload
    const uploadId = Date.now();
    setMessages(prev => [...prev, {
      id: uploadId,
      sender: 'user',
      type: 'xray_upload',
      text: "Uploading X-ray for analysis...",
      fileName: file.name
    }]);

    try {
      const res = await axios.post(`${API_BASE}/predict-xray`, formData);

      const botMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        type: 'xray_result',
        text: res.data.message,
        prediction: res.data.prediction,
        confidence: res.data.confidence,
        imageUrl: `${API_BASE}${res.data.image_url}`,
        lang: 'English'
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: "X-ray analysis failed. Please check the backend connection.",
        sender: 'bot',
        lang: 'English'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([{ id: 1, text: "Chat cleared. Ready for your next query.", sender: 'bot', lang: 'English' }]);
  };

  const renderFormattedText = (text) => {
    if (!text) return "";
    // WhatsApp style bold: *text* -> <strong>text</strong>
    const parts = text.split(/(\*.*?\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('*') && part.endsWith('*')) {
        return <strong key={i} className="font-extrabold">{part.slice(1, -1)}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="flex flex-col h-screen bg-[#f0f2f5] md:bg-gray-100 overflow-hidden font-sans">
      {/* Premium Header */}
      <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 px-4 py-3 flex items-center justify-between z-10 sticky top-0">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-xl shadow-md shadow-blue-100">
            <Activity size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-800 leading-none">TB Expert Global</h1>
            <div className="flex items-center gap-1 mt-1">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-tighter">Medical AI Active</span>
            </div>
          </div>
        </div>


        <div className="flex items-center gap-2">
          {/* RAG Mode Toggle */}
          <button
            onClick={() => setRagMode(!ragMode)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${ragMode
              ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-200'
              : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
              }`}
          >
            {ragMode ? '🧠 RAG Mode' : '⚡ Fast Mode'}
          </button>

          <button onClick={clearChat} className="p-2 text-slate-400 hover:text-red-500 transition-colors">
            <Trash2 size={20} />
          </button>
        </div>
      </header>

      {/* Chat Canvas */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 max-w-4xl mx-auto w-full scrollbar-hidden">
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-3 max-w-[85%] md:max-w-[70%] ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-1 shadow-sm ${msg.sender === 'bot' ? 'bg-white border border-gray-200 text-blue-600' : 'bg-blue-600 text-white'
                  }`}>
                  {msg.sender === 'bot' ? <Bot size={16} /> : <User size={16} />}
                </div>

                <div className={`relative px-4 py-3 rounded-2xl shadow-sm ${msg.sender === 'bot'
                  ? 'bg-white text-slate-800 rounded-tl-none border border-gray-100'
                  : 'bg-blue-600 text-white rounded-tr-none'
                  }`}>
                  {msg.type === 'xray_result' && (
                    <div className="mb-3 overflow-hidden rounded-xl border border-gray-100 shadow-inner bg-gray-50">
                      <img src={msg.imageUrl} alt="X-ray Scan" className="w-full h-48 object-cover" />
                      <div className={`p-3 flex items-center justify-between border-t ${msg.prediction === 'Tuberculosis' ? 'bg-red-50' : 'bg-green-50'
                        }`}>
                        <div className="flex items-center gap-2">
                          {msg.prediction === 'Tuberculosis'
                            ? <AlertCircle className="text-red-600" size={18} />
                            : <CheckCircle2 className="text-green-600" size={18} />
                          }
                          <span className={`font-bold text-xs uppercase tracking-wider ${msg.prediction === 'Tuberculosis' ? 'text-red-700' : 'text-green-700'
                            }`}>
                            AI Result: {msg.prediction}
                          </span>
                        </div>
                        <span className="text-[10px] font-bold text-slate-400">
                          {(msg.confidence * 100).toFixed(1)}% Match
                        </span>
                      </div>
                    </div>
                  )}

                  <p className={`whitespace-pre-wrap leading-relaxed ${msg.lang === 'Urdu' ? 'urdu-text text-lg' : 'text-sm font-medium'
                    }`}>
                    {renderFormattedText(msg.text)}
                  </p>

                  <span className={`text-[8px] mt-1 block opacity-40 uppercase font-bold text-right`}>
                    {new Date(msg.id).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}

          {loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100 flex gap-1">
                <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={chatEndRef} />
      </main>

      {/* Input Dock (WhatsApp Inspired) */}
      <div className="bg-white/80 backdrop-blur-xl border-t border-gray-200 p-4 sticky bottom-0 z-10">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto flex items-end gap-2">
          <div className="flex-1 bg-gray-100 rounded-2xl px-4 py-1.5 flex items-center min-h-[50px] border border-gray-200 focus-within:border-blue-400 focus-within:bg-white transition-all">
            <textarea
              rows="1"
              placeholder={isUrdu(input) ? "...اردو میں پیغام لکھیں" : "Type medical query..."}
              className={`w-full bg-transparent border-none outline-none resize-none py-2 text-slate-800 placeholder:text-slate-400 ${isUrdu(input) ? 'urdu-text text-xl pt-3' : 'text-sm font-medium'
                }`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />

            <label className="p-2 text-slate-400 hover:text-blue-600 cursor-pointer transition-colors">
              <input
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleXrayUpload}
              />
              <Image size={20} />
            </label>
          </div>
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className={`p-3.5 rounded-2xl flex items-center justify-center transition-all shadow-lg ${input.trim() ? 'bg-blue-600 text-white shadow-blue-200 hover:scale-105 active:scale-95' : 'bg-gray-200 text-gray-400'
              }`}
          >
            <Send size={24} />
          </button>
        </form>
        <p className="text-[9px] text-center text-slate-400 mt-2 font-bold uppercase tracking-widest flex items-center justify-center gap-1">
          <Info size={10} />
          Medical Assistance Only • Powered by 200k TB Expert Records
        </p>
      </div>

      <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
      <link href="https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap" rel="stylesheet" />
    </div>
  );
}

export default App;
