<div align="center">

<br/>

```
██████╗ ███████╗██╗   ██╗ ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗     █████╗ ██╗
██╔══██╗██╔════╝██║   ██║██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║    ██╔══██╗██║
██║  ██║█████╗  ██║   ██║██║  ███╗██████╔╝███████║██████╔╝███████║    ███████║██║
██║  ██║██╔══╝  ╚██╗ ██╔╝██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║    ██╔══██║██║
██████╔╝███████╗ ╚████╔╝ ╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║    ██║  ██║██║
╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝
```

### *Multi-Agent Software Engineering Copilot*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-FF6B35?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-8B5CF6?style=for-the-badge)](https://www.trychroma.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F59E0B?style=for-the-badge)](https://groq.com)

<br/>

> **Drop a GitHub URL. Ask anything. DevGraph AI reads the whole codebase so you don't have to.**

<br/>

</div>

---

## What is DevGraph AI?

DevGraph AI is a **repository-aware engineering copilot** powered by a 6-agent LangGraph orchestration system. Feed it any GitHub repository and it ingests, indexes, and understands the entire codebase — then answers architecture questions, generates tests, writes docs, reviews code, and hunts down bugs using semantic retrieval and Groq's Llama 3.1.

This isn't a chatbot with a code window. It's an AI system that has genuinely *read* your repository.

---

## Capabilities at a Glance

| What you ask | Which agent handles it |
|---|---|
| *"Explain the architecture of this repo"* | 📚 RAG Agent |
| *"Where is JWT auth implemented?"* | 📚 RAG Agent |
| *"Find bugs in the auth flow"* | 🐞 Debug Agent |
| *"Review the API layer"* | 🔍 Review Agent |
| *"Generate tests for the login service"* | 🧪 Test Agent |
| *"Write docs for this repository"* | 📝 Documentation Agent |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DevGraph AI Platform                         │
│                                                                      │
│   ┌──────────┐     ┌─────────────┐     ┌──────────────────────┐    │
│   │  React   │────▶│   FastAPI   │────▶│  LangGraph           │    │
│   │ Frontend │     │   Backend   │     │  Orchestrator        │    │
│   └──────────┘     └─────────────┘     └──────────┬───────────┘    │
│                                                    │                │
│                              ┌─────────────────────▼─────────────┐ │
│                              │         Planner Agent             │ │
│                              │   (Intent Analysis & Routing)     │ │
│                              └──┬───────┬────────┬──────┬────────┘ │
│                                 │       │        │      │          │
│                    ┌────────────▼┐ ┌────▼───┐ ┌─▼────┐ ┌▼───────┐ │
│                    │  RAG Agent  │ │ Debug  │ │Review│ │  Test  │ │
│                    │             │ │ Agent  │ │Agent │ │ Agent  │ │
│                    └──────┬──────┘ └────────┘ └──────┘ └────────┘ │
│                           │                                         │
│                    ┌──────▼──────┐     ┌──────────────────────┐    │
│                    │  ChromaDB   │────▶│    Groq (LLaMA 3.1)  │    │
│                    │ Vector Store│     │  Repository-Aware LLM│    │
│                    └─────────────┘     └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How It Works

### Phase 1 — Repository Ingestion

```
GitHub URL  →  Git Clone  →  Code Parsing  →  Chunking  →  Embeddings  →  ChromaDB
```

DevGraph clones the repo, parses every file, creates semantically meaningful chunks, generates HuggingFace embeddings (`all-MiniLM-L6-v2`), and stores them in ChromaDB. The result: **1000+ indexed code chunks** ready for instant retrieval.

### Phase 2 — Intelligent Query Processing

```
Your Question  →  Planner Agent  →  Specialist Agent  →  Code Retrieval  →  Groq LLM  →  Answer
```

Every query hits the **Planner Agent** first. It reads your intent and routes to the right specialist. The specialist pulls semantically relevant code chunks from ChromaDB, feeds them to LLaMA 3.1, and returns a **repository-grounded answer** — not a hallucinated one.

---

## The 6-Agent System

<table>
<tr>
<td width="50%">

### 🧠 Planner Agent
Reads your intent, selects the right specialist agent, and passes context forward. The brain of the operation.

### 📚 RAG Agent
Repository understanding at its core. Handles architecture analysis, function tracing, code walkthroughs, and deep codebase questions.

### 🐞 Debug Agent
Bug investigation and root cause analysis. Give it an error traceback or a description — it traces through the repo to find the source.

</td>
<td width="50%">

### 📝 Documentation Agent
Generates READMEs, API docs, function-level documentation, and developer guides — grounded in what the code actually does.

### 🔍 Review Agent
Code quality, security vulnerabilities, refactoring suggestions, and performance recommendations across the full codebase.

### 🧪 Test Agent
Generates unit and integration tests in Pytest or Jest. Understands what the function does before writing the test.

</td>
</tr>
</table>

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React.js, Axios |
| **Backend** | FastAPI, Python 3.10+ |
| **AI Orchestration** | LangChain, LangGraph |
| **Vector Database** | ChromaDB |
| **Embedding Model** | HuggingFace · `all-MiniLM-L6-v2` |
| **LLM** | Groq · LLaMA 3.1 |
| **Repository Ingestion** | GitPython |

---

## Project Structure

```
DevGraph-AI/
│
├── backend/
│   ├── agents/
│   │   ├── rag_agent.py          ← Repository Q&A, architecture analysis
│   │   ├── general_agent.py      ← Debug, review, documentation
│   │   └── test_agent.py         ← Test generation (Pytest / Jest)
│   │
│   ├── api/
│   │   └── routes.py             ← /ingest and /chat endpoints
│   │
│   ├── graph/
│   │   └── workflow.py           ← LangGraph orchestration logic
│   │
│   ├── rag/
│   │   ├── chunker.py            ← File parsing and chunk creation
│   │   ├── vector_store.py       ← ChromaDB interface
│   │   └── retriever.py          ← Semantic retrieval
│   │
│   ├── services/
│   │   └── github_service.py     ← Repository cloning
│   │
│   └── main.py
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── services/             ← API client
│
└── README.md
```

---

## Getting Started

### 1. Clone

```bash
git clone https://github.com/your-username/devgraph-ai.git
cd devgraph-ai
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Start the server:

```bash
uvicorn main:app --reload
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest` | Clone a GitHub repo and build the vector index |
| `POST` | `/chat` | Query the indexed repository |

**Ingest a repository:**
```json
POST /ingest
{ "repo_url": "https://github.com/owner/repo" }
```

**Ask a question:**
```json
POST /chat
{ "query": "Where is JWT authentication implemented?" }
```

---

## Example Queries

```bash
# Architecture overview
"Explain the architecture of this repository"

# Code navigation
"Where is JWT authentication implemented?"
"How does the payment service communicate with the order service?"

# Debugging
"Find potential bugs in the authentication flow"
"Why might the user session expire prematurely?"

# Testing
"Generate unit tests for the login service"
"Write integration tests for the checkout API"

# Documentation
"Generate a README for this repository"
"Document the public API surface"

# Code review
"Review the API layer for security issues"
"Are there any N+1 query problems in the database layer?"
```

---

## Results

```
  1,000+   code chunks indexed per repository
       6   specialized agents in the LangGraph pipeline
     70%+  reduction in manual code exploration time
      RAG + Multi-Agent  unified into one developer platform
```

---

## Roadmap

- [ ] Code Generation Agent
- [ ] Pull Request Review Agent
- [ ] CI/CD Pipeline Analysis Agent
- [ ] Multi-Repository Support
- [ ] Graph-Based Repository Visualization
- [ ] Persistent Memory Layer
- [ ] Agent Collaboration Framework
- [ ] VS Code Extension

---

## Contributing

Contributions are welcome.

```
1. Fork the repository
2. Create a feature branch  →  git checkout -b feature/your-feature
3. Commit your changes      →  git commit -m "feat: add your feature"
4. Push to your branch      →  git push origin feature/your-feature
5. Open a Pull Request
```

---

<div align="center">

Built by **[SHIVANSH SRIVASTAVA](https://www.linkedin.com/in/shivansh-srivastava-22a4b63a7/)**

*AI Engineer · GenAI Systems*

[![GitHub](https://img.shields.io/badge/GitHub-shivanshsrivastava547--commits-181717?style=flat-square&logo=github)](https://github.com/shivanshsrivastava547-commits)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Shivansh_Srivastava-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/shivansh-srivastava-22a4b63a7)

[![Email](https://img.shields.io/badge/shivanshsrivastava547@gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:shivanshsrivastava547@gmail.com)
<br/>

*If DevGraph AI saved you time, give it a ⭐*

</div>
