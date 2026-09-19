# System Architecture

## 1. Architectural Overview

The **AI Engineering Assistant** is designed as a desktop-first system that transforms natural-language Thai requirements into structured, actionable English prompts for AI coding agents.

### High-Level Topology

```text
┌─────────────────────────────────────────────────────────────────┐
│                 Desktop Application (Primary)                   │
│         (Tauri 2 Core + Svelte 5 UI + Strict TypeScript)        │
└────────────────────────────────┬────────────────────────────────┘
                                 │ HTTP (Local loopback 127.0.0.1:8000)
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AI Service Backend                          │
│                   (Python 3.13 + FastAPI)                       │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │   API Layer      │  │  Prompt Engine   │  │  AI Agents    │  │
│  │  (/health, /v1)  │  │   (Boundaries)   │  │ (Boundaries)  │  │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬───────┘  │
│           │                     │                    │          │
│  ┌────────▼─────────────────────▼────────────────────▼───────┐  │
│  │               LLM Provider Abstraction                    │  │
│  │      (BaseLLMProvider: Cloud Providers & Local Models)    │  │
│  └──────────────────────────────┬────────────────────────────┘  │
│                                 │                               │
│  ┌──────────────────────────────┴────────────────────────────┐  │
│  │                     Domain / Application                  │  │
│  └──────────────────────────────┬────────────────────────────┘  │
│                                 │                               │
│  ┌──────────────────────────────┴────────────────────────────┐  │
│  │                  Repository Abstraction                   │  │
│  │                 (IRepository[T] Interface)                │  │
│  └──────────────────────────────┬────────────────────────────┘  │
│                                 │                               │
│  ┌──────────────────────────────┴────────────────────────────┐  │
│  │                     SQLite Repository                     │  │
│  │       (Standard Library sqlite3, Parameterized SQL)       │  │
│  └──────────────────────────────┬────────────────────────────┘  │
└─────────────────────────────────┼───────────────────────────────┘
                                  ▼
                   ┌─────────────────────────────┐
                   │       SQLite Database       │
                   │    (Embedded data/app.db)   │
                   │ [Zero Server / Zero Docker] │
                   └─────────────────────────────┘
                                  :
                   ┌ - - - - - - - - - - - - - - ┐
                   │    Qdrant Vector Store      │
                   │  (Deferred to Milestone 5)  │
                   └ - - - - - - - - - - - - - - ┘
```

---

## 2. Separation of Concerns & Boundary Rules

1. **Frontend Isolation**:
   - The desktop frontend (`apps/desktop`) handles UI interaction, state visualization, and prompt editing.
   - The frontend communicates exclusively with the local AI Service API via loopback.
   - The frontend **never** connects directly to the SQLite database file or LLM providers.
   - No business logic is placed directly inside UI components.

2. **AI Service Modular Design**:
   - The AI Service (`apps/ai-service`) is organized into discrete domain layers:
     - `app/api`: HTTP routing and serialization.
     - `app/core`: Configuration and logging.
     - `app/domain`: Lightweight domain models and contracts.
     - `app/llm`: Provider-agnostic abstraction interface.
     - `app/repositories`: Database access boundaries.
     - `app/services`: Application workflows and business orchestration.

3. **Desktop-First SQLite Persistence**:
   - SQLite is embedded directly in the AI Service process.
   - Standard library `sqlite3` is used with parameterized queries and explicit connection lifecycle management (`WAL` mode enabled).
   - Zero ORM, zero heavy migration framework, and zero external database process required.
   - The domain layer depends only on `IRepository[T]`, making future storage migrations possible without domain code changes.

4. **Future Knowledge & RAG Strategy (M5)**:
   - In M1, `BaseKnowledgeRetriever` in `app/rag/base.py` establishes the contract.
   - Qdrant will be introduced strictly in Milestone 5 (Knowledge / RAG) as an optional sidecar/container for vector indexing.
