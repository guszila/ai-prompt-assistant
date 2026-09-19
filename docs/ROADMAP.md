# Project Roadmap & Milestones (M1–M9)

This document tracks the phased development of the **AI Engineering Assistant**.

---

## Milestone 1: Foundation [COMPLETED]
- [x] Monorepo repository structure (`apps/*`, `packages/*`, `data/*`, `docs/*`).
- [x] Tauri 2 + Svelte 5 + TypeScript desktop scaffold with modular UI shell.
- [x] Python 3.13 + FastAPI AI service with `/health` endpoint and test suite.
- [x] Embedded SQLite persistence foundation using standard library `sqlite3` + repository abstraction (`IRepository[T]`).
- [x] Provider-agnostic LLM interface abstraction (`BaseLLMProvider`).
- [x] Lightweight domain contracts & shared TypeScript types.
- [x] Zero external database server or Docker dependency for core desktop execution.
- [x] Project documentation & agent guidelines (`AGENTS.md`).

---

## Milestone 2: Core Prompt Engine [COMPLETED]
- [x] Deterministic 5-stage prompt transformation pipeline:
  - `RequirementNormalizer`: Unicode normalization, whitespace collapsing, Thai/English/mixed language detection.
  - `RequirementAnalyzer`: Intent extraction, entity & action recognition, explicit constraint extraction without fabrication.
  - `EngineeringTerminologyMapper`: Separation of Authentication from Authorization, generic API from RESTful API, inferred concepts tagged with explicit Assumptions.
  - `AmbiguityDetector`: Functional ambiguity detection and targeted clarification questions without speculative tech stack demands.
  - `PromptComposer`: Deterministic Markdown assembly, omission of empty sections, formalization of acceptance criteria without invented performance metrics.
  - `PromptValidator`: Integrity checks against missing fields, isolated assumptions, and ungrounded latency/throughput metrics.
- [x] FastAPI endpoint `POST /v1/prompts/analyze` with `PromptService` coordination.
- [x] Shared TypeScript contracts (`@ai-assistant/shared-types`, `@ai-assistant/prompt-engine`) and JSON Schemas (`requirement-analysis.schema.json`).
- [x] Comprehensive test suite (42 automated unit, integration, deterministic, and API tests).

---

## Milestone 3: LLM Integration [COMPLETED]
- [x] Provider-agnostic LLM interface (`BaseLLMProvider`) supporting structured JSON generation.
- [x] Deterministic `MockLLMProvider` for reliable offline testing and failure simulation.
- [x] `OpenAICompatibleProvider` implemented via `httpx` with bounded retries and exponential backoff.
- [x] Security-hardened configuration using `pydantic.SecretStr` and sanitization in logs/errors.
- [x] Untrusted model candidate boundary (`LLMRequirementCandidate`).
- [x] `GroundingReconciler` enforcing strict priority: Explicit User Input > M2 Deterministic Baseline > LLM Candidate.
- [x] Robust grounding safeguards: AuthN != AuthZ, generic API != RESTful API, blocking ungrounded database/tech and performance metric hallucinations.
- [x] Graceful degradation: Failures originating from the optional LLM enhancement layer automatically fall back to the M2 deterministic baseline with typed failure reasons (`LLMFallbackReason`).
- [x] Complete automated test suite (69 tests covering providers, reconciler, fallback modes, security sanitization, and M1/M2 regression).

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
