# AI Content Production Copilot

An enterprise-grade, multi-agent AI editorial platform designed to assist writers and content production teams at digital publishers (e.g., Pocket FM, Pocket Entertainment). 

This platform automates the core publishing cycle: **Consistency Checking & Planning $\rightarrow$ Line Editing & Prose Refinement $\rightarrow$ Idiomatic Translation & Localization $\rightarrow$ Synthetic Audiobook Production**.

---

## 🌟 Architecture Overview

```
                      +-------------------+
                      |    Streamlit UI   |
                      +---------+---------+
                                |
                                | REST (HTTP)
                                v
                      +---------+---------+
                      |  FastAPI Backend  |
                      +---------+---------+
                                |
                                | Runs Graph Workflow
                                v
               +----------------+----------------+
               |        LangGraph Pipeline       |
               |                                 |
               |  [Planner] -> Check Lore        |
               |       |                         |
               |       v                         |
               |  [Reviewer] -> Polishes Text    |
               |       |                         |
               |       v                         |
               |  [Translator] -> Localizes      |
               |       |                         |
               |       v                         |
               |  [TTS Agent] -> Speech Audio    |
               +----------------+----------------+
                                |
                                | Exports
                                v
                      +---------+---------+
                      |   outputs/ folder |
                      |  (MD text & MP3)  |
                      +-------------------+
```

---

## 📁 Repository Layout

The system is organized to decouple orchestration, logic interfaces, and clients, ensuring scalability:

```text
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point & static files config
│   │   ├── config.py               # Environment validation (Pydantic Settings)
│   │   ├── schemas/
│   │   │   └── story.py            # API request/response validation schemas
│   │   ├── routers/
│   │   │   └── copilot.py          # API Endpoint routers (/run, /refine, /translate, /tts)
│   │   ├── services/
│   │   │   ├── llm.py              # LLM Service Client wrapper (Groq SDK)
│   │   │   ├── translation.py      # Translation Interface & Google Translate wrapper
│   │   │   └── tts.py              # Edge-TTS Neural Voice synthesis interface
│   │   ├── agents/
│   │   │   ├── state.py            # State tracker definition (CopilotState)
│   │   │   ├── graph.py            # LangGraph workflow compilation
│   │   │   ├── planner.py          # Node: Lore consistency & outline feedback agent
│   │   │   ├── reviewer.py         # Node: Editorial line editor agent
│   │   │   ├── translator.py       # Node: Localization agent
│   │   │   └── tts_agent.py        # Node: Audio narration rendering agent
│   │   └── prompts/
│   │       ├── planner_prompts.py
│   │       ├── reviewer_prompts.py
│   │       └── translator_prompts.py
│   ├── requirements.txt            # Backend dependencies
│   └── Dockerfile                  # API service image specification
├── frontend/
│   ├── app.py                      # Interactive Streamlit application interface
│   ├── styles.css                  # Custom styling (Glassmorphism / Dark Mode)
│   └── Dockerfile                  # Frontend container configuration
├── outputs/
│   ├── stories/                    # Persistent storage of edited markdown files
│   └── audio/                      # Persistent storage of exported MP3 voice narrations
├── docker-compose.yml              # Multi-container local orchestration script
└── README.md
```

---

## 🤖 Agent Roles & Graph Nodes

1. **Planner Node (`planner.py`)**: Evaluates raw writer drafts against context (Series Bible) for spelling inconsistencies, factual contradictions, and pacing blocks. Outputs structured Markdown feedback.
2. **Reviewer Node (`reviewer.py`)**: Rewrites the raw draft, addressing all points in the planner feedback. Refines sentence structure, enhances descriptions, and polishes dialogue.
3. **Translator Node (`translator.py`)**: Translates refined English chapters into target languages (e.g., Tamil, Spanish, Hindi) while maintaining idiomatic flow, tone, and character context.
4. **TTS Node (`tts_agent.py`)**: Converts the translated (or refined) chapter into high-fidelity neural MP3 audio using Microsoft Edge Neural TTS.

---

## ⚡ API Specifications

FastAPI exposes the following REST APIs:

### 1. Execute Full Multi-Agent Pipeline
* **Endpoint**: `POST /api/copilot/run`
* **Request Body**:
  ```json
  {
    "original_draft": "Rohan went into the study. Sarah said she was angry...",
    "genre": "Sci-Fi",
    "target_audience": "Young Adults",
    "language": "Tamil",
    "voice": "Female",
    "series_bible": "Sarah hates when people make excuses. Rohan is former agent."
  }
  ```
* **Response Body**:
  ```json
  {
    "session_id": "ab90cd12ef34",
    "planner_feedback": "# Consistency Check...",
    "refined_draft": "Rohan slipped into the dimly lit study...",
    "localized_draft": "ரோஹன் மெதுவாகப் படிக்கும் அறைக்குள் நுழைந்தான்...",
    "audio_url": "http://localhost:8000/static/audio/audio_tamil_female.mp3",
    "logs": [
      "System: Workflow initialized for session ab90cd12ef34.",
      "PlannerNode: Consistency check and improvement planning completed.",
      "ReviewerNode: Story refinement and line editing completed.",
      "TranslatorNode: Localized chapter translation into Tamil completed.",
      "TTSNode: Narration audiobook generated successfully."
    ]
  }
  ```

### 2. Standalone Endpoints
* `POST /api/copilot/refine`: Performs outline analysis and draft styling only.
* `POST /api/copilot/translate`: Takes text and translates to a target language.
* `POST /api/copilot/tts`: Generates speech files from given text.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- A **Groq API Key** (Set as environment variable `GROQ_API_KEY`)

### Local Installation

1. **Clone the Repository** and navigate to directory:
   ```bash
   git clone <repository_url>
   cd ai-content-copilot
   ```

2. **Set up the Backend**:
   ```bash
   # Navigate to backend directory
   cd backend
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment variables**:
   Create a `.env` file inside the `backend/` directory:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   GROQ_MODEL=llama3-70b-8192
   ```

4. **Launch the Backend API Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The backend API will run at `http://127.0.0.1:8000`. You can inspect the Swagger UI docs at `http://127.0.0.1:8000/docs`.

5. **Launch the Frontend Client**:
   Open a new terminal tab and run:
   ```bash
   cd frontend
   pip install streamlit httpx
   streamlit run app.py --server.port 8501
   ```
   Access the web app UI at `http://localhost:8501`.

---

## 🐳 Docker Deployment

To launch the multi-container configuration:
1. Export your API Key:
   ```bash
   export GROQ_API_KEY="your_groq_key"
   ```
2. Build and launch:
   ```bash
   docker-compose up --build
   ```
3. Visit the frontend at `http://localhost:8501`.

---

## 🛠️ Production Best Practices & Architectural Scalability

1. **Decoupled Interfaces (Service Layer Pattern)**: LLM operations, translations, and audio renders are tucked behind clean service layers. Changing voice engines (e.g. from Edge-TTS to ElevenLabs or a local Coqui-XTTS server) only requires changing the implementation of `BaseTTSService`, leaving graph logic untouched.
2. **Robust Content Chunking**: Translating large scripts can hit size limits or cost boundaries. The translation layer implements paragraph-level chunking to maintain reliability under large chapters.
3. **Structured Outputs**: Uses Pydantic to structure and clean REST API payloads, validating data before starting LLM iterations.
4. **Local Event Loop Control**: Avoids standard event loop blockage in FastAPI when calling async audio render engines (`edge-tts`) by encapsulating async synthesis loops.

---

## 📈 Future Scalability & Enhancements

- **Long-term Character Consistency**: Integrating a Vector Database (like Qdrant/pgvector) or a Graph Database (Neo4j) to dynamically query character profiles and story continuity graphs.
- **Async Task Queueing**: Migrating synchronous endpoints to asynchronous Celery/Redis tasks, returning a job ID to the frontend to poll for state completion.
- **LoRA Fine-tuning**: Fine-tuning Qwen/Llama models on specific author scripts to automatically replicate publisher brand voices.

---

## 📄 Resume-Worthy Project Details

**AI Content Production Copilot (Lead AI Engineer)**
* **Stack**: LangGraph, FastAPI, Streamlit, Groq (Llama-3), Edge-TTS, Pydantic, Docker.
* **Orchestration**: Designed a stateful multi-agent system utilizing LangGraph to model editorial content workflows (Planner $\rightarrow$ Editor $\rightarrow$ Translator $\rightarrow$ Text-to-Speech), streamlining raw drafts into localized, narrated audiobooks.
* **Engineering Achievements**:
  - Implemented service decoupling using abstract base classes for hot-swappable TTS and translation engines.
  - Mitigated translation/LLM context limits for book chapters by implementing paragraph-level chunking and batch synthesis.
  - Packaged application using Docker-Compose to support scalable development and containerized service isolation.
