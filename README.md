# 🎓 AI Tutor - Grade 10 NCERT

An intelligent AI-powered tutoring system for Grade 10 students, covering **Mathematics, Physics, and Chemistry** based on NCERT curriculum.

**Demo** [Streamlit Web App](https://ai-tutor-grade10-ncert-play.streamlit.app/) 
**Created by:** Piyush Sharma 

---

## Features

- **Multi-Subject Support**: Maths, Physics, Chemistry (Grade 10 NCERT)
- **Powered by Groq Llama 3.3** (70B parameters)
- **Smart Retrieval**: FAISS vector search on NCERT content
- **Conversational Memory**: Remembers your learning journey
- **User Profiles**: Personalized experience with SQLite
- **Export Chats**: Download conversation history
- **Responsible AI**: Content filtering for educational safety
- **Modern UI**: Beautiful, student-friendly design

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq Llama 3.3 (70B) |
| Embeddings | HuggingFace Sentence Transformers |
| Vector Store | FAISS |
| Framework | LangChain |
| Database | SQLite |
| Frontend | Streamlit |
| Content | NCERT Class 10 Textbooks |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/AI-Tutor-Project.git
cd AI-Tutor-Project
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the app**
```bash
streamlit run app.py
```

---

## Project Structure
```
AI-Tutor-Project/
├── app.py                          # Main Streamlit application
├── src/
│   ├── chains/
│   │   └── tutor_chain.py          # LangChain conversation chain
│   ├── retrieval/
│   │   ├── build_vector_store.py   # FAISS index builder
│   │   └── query_vectorstore.py    # Vector retrieval interface
│   ├── memory/
│   │   └── user_database.py        # SQLite user management
│   └── safety/
│       └── content_filter.py       # Content safety filter
├── data/
│   ├── raw_content/                # NCERT PDF textbooks
│   ├── vector_store/               # FAISS index files
│   └── users.db                    # User database
├── requirements.txt
└── README.md
```

---

## Usage

1. **Login**: Enter your name to start
2. **Ask Questions**: Type questions about Grade 10 subjects
3. **Quick Questions**: Use sidebar buttons for sample queries
4. **Export Chat**: Download your learning history
5. **Track Progress**: See your message count and streak

---

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

---

## License

MIT License - Free for educational use

---

## Author

**Piyush Sharma**  
Passionate about AI 

Connect: [LinkedIn](https://www.linkedin.com/in/piyush-sharma7444/) | [GitHub](https://github.com/sharma-piyush1) | [Portfolio](coming...)

---

## Acknowledgments

- NCERT for educational content
- Groq for free LLM API access
- LangChain community
- Streamlit for amazing framework

---

⭐ **Star this repo if you find it helpful!**
