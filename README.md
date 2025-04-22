
# 🚀 OSINT LangChain App: Hybrid Threat Intelligence Dashboard

**OSINT-LangChain App** is a robust, open-source Threat Intelligence (TI) application designed to collect, analyse, and visualise cybersecurity threats using advanced Retrieval-Augmented Generation (RAG) techniques, powered by LangChain, OpenAI, ChromaDB, and Streamlit.

## 📌 Overview
This repository hosts a Hybrid Threat Intelligence Dashboard application capable of:
- Fetching threat intelligence feeds from multiple OSINT sources.
- Automatically analysing and summarising threats using advanced LLMs (OpenAI GPT-4o).
- Storing and indexing threat data in both structured (SQLite) and vector-based (ChromaDB) databases.
- Providing semantic search capabilities for intuitive and precise threat discovery.
- Delivering an interactive RAG-powered chatbot for context-rich threat queries and insights.

## 🎯 Features
- **Automated OSINT Feeds Ingestion**
- **Advanced AI Analysis (GPT-4o)**
- **Hybrid Data Storage (SQLite & ChromaDB)**
- **Semantic Threat Search**
- **Interactive Threat Chatbot (RAG)**
- **Enhanced UI/UX (Streamlit, Custom CSS)**

## 🛠️ Technology Stack
- **UI:** Streamlit
- **AI/RAG:** LangChain, OpenAI GPT-4o
- **Databases:** SQLite, ChromaDB
- **Processing:** Pandas, Feedparser, Requests
- **Environment:** Python Virtual Environment

## 🚧 Installation
Clone, set up virtual environment, install dependencies, configure environment variables, and run:
```
streamlit run dashboard.py
```

## 🚀 Usage
- **Fetch & Analyse Latest Threats:** Sidebar button
- **Structured Threat Database:** SQLite view and sorting
- **Semantic Search:** Intuitive natural language queries
- **Chatbot:** Interactive queries with context-aware responses

## 📁 Project Structure
```
osint-langchain-app/
├── chroma_db/
├── database.py
├── chromadb_utils.py
├── feed_utils.py
├── analysis_utils.py
├── dashboard.py
├── chatbot.py
├── requirements.txt
└── README.md
```

## 📌 Roadmap
- Additional OSINT/TI sources
- Real-time processing
- User authentication and collaboration
- Enhanced visualisation
- Docker containerisation

## 🤝 Contributing
Fork, branch, commit, push, and PR!

## 📝 License
MIT License

## 📬 Contact
- **GitHub:** [MikeTigerBlue](https://github.com/miketigerblue)
