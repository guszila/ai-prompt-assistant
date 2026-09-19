# Project Roadmap & Milestones (M1–M9)

This document tracks the phased development of the **AI Engineering Assistant**.

---

## Milestone 1: Foundation [CURRENT]
- [x] Monorepo repository structure (`apps/*`, `packages/*`, `data/*`, `docs/*`).
- [x] Tauri 2 + Svelte 5 + TypeScript desktop scaffold with modular UI shell.
- [x] Python 3.13 + FastAPI AI service with `/health` endpoint and test suite.
- [x] Embedded SQLite persistence foundation using standard library `sqlite3` + repository abstraction (`IRepository[T]`).
- [x] Provider-agnostic LLM interface abstraction (`BaseLLMProvider`).
- [x] Lightweight domain contracts & shared TypeScript types.
- [x] Zero external database server or Docker dependency for core desktop execution.
- [x] Project documentation & agent guidelines (`AGENTS.md`).

---

## Milestone 2: Core Prompt Engine
- [ ] Core prompt transformation pipeline (Thai requirements to structured prompts).
- [ ] Prompt templates and markdown preview interface in desktop UI.
- [ ] Direct loopback integration between desktop and AI service.

---

## Milestone 3: LLM Integration
- [ ] Cloud LLM provider implementations (Anthropic Claude, OpenAI, Google Gemini).
- [ ] Streaming response support.
- [ ] Provider configuration and API key management.

---

## Milestone 4: Prompt Quality System
- [ ] Heuristics and validation rules for prompt completeness.
- [ ] Ambiguity detection and automated clarification queries.
- [ ] Prompt quality scoring.

---

## Milestone 5: Knowledge / RAG
- [ ] Introduction of **Qdrant** vector database.
- [ ] Semantic indexing of software engineering prompt templates.
- [ ] Grounded retrieval of framework standards and architecture patterns.

---

## Milestone 6: Multi-Agent System
- [ ] Requirement Analyzer agent.
- [ ] Engineering Translator agent.
- [ ] Prompt Architect agent.
- [ ] Prompt Reviewer agent.

---

## Milestone 7: Learning System
- [ ] Experience data collection from user interactions.
- [ ] User edit tracking and diff view.
- [ ] Quality filtering and dataset curation pipeline.

---

## Milestone 8: Model Improvement
- [ ] Benchmark evaluation datasets in `data/evaluation`.
- [ ] Regression test suite for model outputs.
- [ ] Fine-tuning dataset generation.

---

## Milestone 9: Local AI
- [ ] Local open-weight model provider (Ollama / vLLM / llama.cpp).
- [ ] Full offline execution mode.
- [ ] In-app model switching.
