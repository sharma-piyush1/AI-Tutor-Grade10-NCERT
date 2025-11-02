"""
AI-Tutor - Streamlit Web Application
Grade 10 NCERT (Physics, Chemistry, Maths)
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))
from chains.tutor_chain import AITutor as tutor_Chain
from memory.user_database import UserDatabase
from safety.content_filter import ContentFilter  

st.set_page_config(
    page_title="AI Tutor - Grade 10 NCERT",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glassmorphism Chat Container */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
       
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput input {
        border-radius: 15px;
        border: 2px solid #667eea;
        padding: 1rem;
        font-size: 1rem;
    }
    
    /* Chat Input */
    .stChatInputContainer {
        border-radius: 25px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #FFD700 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* Success/Warning Messages */
    .stAlert {
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Title Animation */
    .title-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Subject Badges */
    .subject-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .math-badge { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
    .physics-badge { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
    .chemistry-badge { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; }
    
    /* Footer */
    footer {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database and content filter
if "db" not in st.session_state:
    st.session_state.db = UserDatabase()
    st.session_state.content_filter = ContentFilter()

# User Authentication
if "user_id" not in st.session_state:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("🎓 Welcome to AI Tutor")
    st.markdown("---")
    
    username = st.text_input("Enter your name to start learning:", placeholder="e.g., Rahul, Priya")
    
    if st.button("Start Learning", use_container_width=True):
        if username and len(username.strip()) > 0:
            user_id = st.session_state.db.create_user(username.strip())
            st.session_state.user_id = user_id
            st.session_state.username = username.strip()
            st.rerun()
        else:
            st.error("Please enter your name!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Initialize tutor and load history
if "tutor" not in st.session_state:
    with st.spinner("Initializing AI Tutor..."):
        st.session_state.tutor = tutor_Chain()
    
    # Load previous conversation
    history = st.session_state.db.get_user_history(st.session_state.user_id)
    st.session_state.messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    st.session_state.conversation_started = len(history) > 0  # Fixed: initialize this variable

# Sidebar
with st.sidebar:
    st.title(f"{st.session_state.username}")
    
    # User stats
    stats = st.session_state.db.get_user_stats(st.session_state.user_id)
    st.metric("Total Messages", stats["total_messages"])
    
    st.markdown("---")
    
    # About
    st.header("About")
    st.info("""
    **AI Tutor for Grade 10 NCERT**
            
    **Powered by:**
    - Groq Llama 3.3 (70B)
    - FAISS Vector Search
    - LangChain Framework
    - NCERT Textbooks
    """)
    
    st.header("Available Topics")
    with st.expander("Mathematics"):
        st.markdown("""
        - Quadratic Equations
        - Standard Form
        - Solving Methods
        - Real-life Applications
        """)
        
    with st.expander("Physics"):
        st.markdown("""
        - Light - Reflection & Refraction
        - Spherical Mirrors
        - Image Formation
        - Mirror Formula
        """)

    with st.expander("Chemistry"):
        st.markdown("""
        - Chemical Reactions
        - Types of Reactions
        - Balancing Equations
        - Conservation of Mass
        """)
    
    st.markdown("---")
    
    # Sample questions
    st.header("Try These")
    sample_questions = [
        "What is the quadratic formula?",
        "Explain laws of reflection",
        "Types of chemical reactions?",
        "How do concave mirrors work?",
        "Solve: x² - 5x + 6 = 0"
    ]

    for q in sample_questions:
        if st.button(q, key=f"sample_{q[:15]}", use_container_width=True):
            st.session_state.selected_question = q
    
    st.markdown("---")
    
    # Export conversation
    if st.button("Export Chat", use_container_width=True):
        export_text = st.session_state.db.export_conversation(st.session_state.user_id)
        st.download_button(
            "Download as TXT",
            export_text,
            file_name=f"ai_tutor_{st.session_state.username}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Clear conversation
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.db.clear_user_history(st.session_state.user_id)
        st.session_state.tutor.clear_history()
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()
    
    # Logout
    if st.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Main Chat
st.title("AI Tutor - Grade 10 NCERT")
st.markdown("---")

# Welcome message
if not st.session_state.conversation_started:
    st.markdown("""
    **Welcome to AI Tutor!** 
    
    I can help you with Grade 10 NCERT subjects:
    - 📐 **Mathematics** - Quadratic equations, algebra
    - 🔬 **Physics** - Light, reflection, mirrors
    - ⚗️ **Chemistry** - Chemical reactions, equations
    
    **Guidelines:**
    - Ask educational questions only
    - I focus on concepts, not just answers
    - Ask follow-ups - I remember our conversation!
    
    Let's start learning! 
    """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle sample question
if "selected_question" in st.session_state:
    prompt = st.session_state.selected_question
    del st.session_state.selected_question
else:
    prompt = None

# Chat input
if user_input := st.chat_input("Ask your question..."):
    prompt = user_input

if prompt:
    st.session_state.conversation_started = True
    
    # Content safety check
    is_safe, safety_msg = st.session_state.content_filter.is_safe(prompt)
    
    if not is_safe:
        with st.chat_message("assistant"):
            st.warning(safety_msg)
        st.stop()
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.db.save_message(st.session_state.user_id, "user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.tutor.ask(prompt)
            
            if response:
                # Add safety context
                response = st.session_state.content_filter.add_safety_context(response)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.db.save_message(st.session_state.user_id, "assistant", response)
            else:
                error_msg = "Error processing your question. Please try again."
                st.markdown(error_msg)

# Footer
st.markdown("---")
st.caption("""
**AI Tutor for Grade 10 NCERT** | Created with ❤️ by **Piyush Sharma** 
Built using: LangChain • Groq • FAISS • Streamlit • SQLite | Responsible AI Enabled
""")