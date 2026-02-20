import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
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
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
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
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot with knowledge base"""
    # Get TB knowledge
    knowledge = get_knowledge_base()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(knowledge)
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
    )
    
    # Create vector store
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="./tb_chroma_db"
    )
    
    return vectorstore

def get_response_simple(query, vectorstore):
    """Get response using vector similarity search"""
    docs = vectorstore.similarity_search(query, k=3)
    
    # Combine relevant documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create a simple response
    response = f"Based on the TB medical knowledge:\n\n{context}\n\n"
    response += "For personalized medical advice, please consult a healthcare professional."
    
    return response

def main():
    # Header
    st.markdown('<div class="main-header">🩺 TB Healthcare Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI-powered guide for Tuberculosis information</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=TB+Bot", use_column_width=True)
        st.title("About TB Bot")
        st.write("""
        This chatbot provides comprehensive information about Tuberculosis (TB) including:
        - Symptoms and diagnosis
        - Types of TB
        - Treatment options
        - Prevention methods
        - Nutrition guidance
        """)
        
        st.markdown("---")
        st.markdown("### Quick Links")
        st.markdown("- [WHO TB Facts](https://www.who.int/tb)")
        st.markdown("- [National TB Helpline: 1800-11-6666](tel:1800116666)")
        
        st.markdown("---")
        st.warning("⚠️ This is for informational purposes only. Always consult a healthcare professional for medical advice.")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Ask Your TB-Related Questions")
        
        # Initialize chatbot
        with st.spinner("Loading TB knowledge base..."):
            vectorstore = initialize_chatbot()
        
        # Chat interface
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about Tuberculosis..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_response_simple(prompt, vectorstore)
                    st.markdown(response)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Quick action buttons
        st.markdown("---")
        st.markdown("#### 🔍 Quick Questions")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("What are TB symptoms?"):
                st.session_state.messages.append({"role": "user", "content": "What are the symptoms of TB?"})
                st.rerun()
        
        with col_b:
            if st.button("How is TB treated?"):
                st.session_state.messages.append({"role": "user", "content": "How is TB treated?"})
                st.rerun()
        
        with col_c:
            if st.button("How to prevent TB?"):
                st.session_state.messages.append({"role": "user", "content": "How can I prevent TB?"})
                st.rerun()
    
    with col2:
        st.markdown("### 📊 TB Quick Facts")
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**🦠 Causative Agent**")
        st.write("*Mycobacterium tuberculosis* bacteria")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**⏱️ Treatment Duration**")
        st.write("6-9 months of regular medication")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**✅ Cure Rate**")
        st.write("Over 95% with proper treatment")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**⚠️ Warning Signs**")
        st.write("- Cough > 3 weeks\n- Blood in sputum\n- Night sweats\n- Weight loss")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📞 Emergency Contacts")
        st.info("""
        **National TB Helpline (India)**  
        📞 1800-11-6666 (Toll-free)
        
        **WHO TB Helpline**  
        📞 +41 22 791 21 11
        """)
        
        st.markdown("---")
        if st.button("🔄 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
