# AI Engineering Assistant

> Transforming natural-language Thai requirements into precise, structured English prompts optimized for software engineering and AI coding agents.

---

## 1. Project Overview

**AI Engineering Assistant** is a desktop application designed to bridge the gap between human engineering intent in Thai and actionable, technically precise prompts for AI coding agents.

### Core Capabilities (Phased):
- Understand Thai software requirements.
- Extract technical intent and identify ambiguity.
- Transform informal descriptions into rigorous software engineering specifications.
- Generate structured engineering prompts with explicit constraints and testability criteria.
- Local, self-contained desktop persistence with zero required server setup.

---

## 2. Technology Architecture

```text
Desktop Application (Primary)
    │
    ├── Tauri 2
    │
    ├── Svelte 5 (Runes)
    │
    └── TypeScript (Strict)
            │
            ▼ Local Loopback HTTP (127.0.0.1:8000)
       AI Service
            │
            └── Python 3.13 + FastAPI
                    │
                    ├── AI Agents (Modular boundaries)
                    ├── Prompt Engine (Validation & templates)
                    ├── LLM Providers (Provider-agnostic abstraction)
                    ├── RAG Boundary (Knowledge retrieval - deferred to M5)
                    └── Repository Boundary (IRepository[T])
                            │
                            ▼
                     SQLite Database (Embedded local app.db file)
                     [Zero external database server, zero Docker needed]
```

---

## 3. Repository Structure

```text
ai-prompt-assistant/
├── apps/
│   ├── desktop/                         # Tauri 2 + Svelte 5 + TypeScript desktop app
│   └── ai-service/                      # Python + FastAPI AI backend service
│
├── packages/
│   ├── shared-types/                    # Shared TypeScript domain interfaces & types
│   ├── prompt-engine/                   # Foundational prompt engine package
│   └── schemas/                         # Foundational JSON validation schemas
│
├── infrastructure/
│   └── README.md                        # Desktop-first architecture guidelines
│
├── data/                                # Local data storage (app.db gitignored)
│   ├── raw/                             # Raw requirement samples
│   ├── processed/                       # Cleaned data
│   ├── datasets/                        # Formatted training/eval datasets
│   └── evaluation/                      # Evaluation benchmark test cases
│
├── docs/                                # Technical documentation
│   ├── ARCHITECTURE.md                  # System architecture and boundary rules
│   ├── REQUIREMENTS.md                  # Functional & non-functional requirements
│   ├── DATA_MODEL.md                    # Domain entities & SQLite persistence
│   ├── AI_ARCHITECTURE.md               # Agent workflows and LLM provider interfaces
│   └── ROADMAP.md                       # Phased roadmap from M1 to M9
│
├── scripts/                             # Development helper scripts
├── tests/                               # Integration tests
├── .env.example                         # Environment configuration blueprint
├── .gitignore                           # Git ignore rules
├── AGENTS.md                            # Rules and conventions for AI coding agents
└── README.md
```

---

## 4. Getting Started

### Prerequisites
- **Node.js**: v20+ (v22 recommended) and `npm`
- **Python**: 3.11+ (Python 3.13 supported)
- **Rust**: 1.77+ with Cargo (installed via Rustup; native Windows `.exe` bundle compilation requires Visual Studio C++ Build Tools)

> [!NOTE]
> No Docker or database server is required to run the application. Local storage uses embedded SQLite (`data/app.db`).

### AI Service (FastAPI)
```powershell
cd apps/ai-service
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Health check endpoint: `http://127.0.0.1:8000/health`

### Desktop Application (Svelte 5 + Tauri 2)
```powershell
cd apps/desktop
npm install
npm run dev        # Run Vite web preview
npm run check      # Run TypeScript & Svelte diagnostics
npm run build      # Build frontend production bundle
```

---

## 5. Phased Roadmap (M1–M9)

- **M1 — Foundation**: ✅ Current Milestone (Monorepo, Svelte 5 desktop shell, FastAPI AI service, SQLite persistence foundation, domain contracts, and agent rules).
- **M2 — Core Prompt Engine**: Prompt transformation pipeline (Thai requirements to structured prompts).
- **M3 — LLM Integration**: Cloud LLM providers (Anthropic, OpenAI, Gemini) via `BaseLLMProvider`.
- **M4 — Prompt Quality System**: Heuristics, ambiguity detection, and prompt scoring.
- **M5 — Knowledge / RAG**: Introduction of Qdrant vector database and semantic prompt template retrieval.
- **M6 — Multi-Agent System**: Requirement Analyzer, Engineering Translator, Prompt Architect, and Prompt Reviewer agents.
- **M7 — Learning System**: User feedback collection and experience data curation.
- **M8 — Model Improvement**: Benchmark evaluation datasets and fine-tuning data pipelines.
- **M9 — Local AI**: Local open-weight models (Ollama / vLLM / llama.cpp) for full offline execution.