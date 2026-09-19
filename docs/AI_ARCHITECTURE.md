# AI Architecture & LLM Abstraction

## 1. Provider-Agnostic LLM Abstraction

To ensure long-term independence from specific vendors, the system decouples prompt workflows from underlying models via the `BaseLLMProvider` abstract interface.

```text
┌─────────────────────────────────────────────────────────────┐
│                    BaseLLMProvider (ABC)                    │
├─────────────────────────────────────────────────────────────┤
│ + generate(prompt: str, options: dict) -> LLMResponse       │
│ + generate_stream(prompt: str, options: dict) -> AsyncGen   │
│ + get_model_info() -> ModelInfo                             │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ Anthropic    │        │ OpenAI /     │        │ Local LLM    │
│ Provider     │        │ Gemini       │        │ (Ollama/vLLM)│
└──────────────┘        └──────────────┘        └──────────────┘
```

---

## 2. Multi-Agent Pipeline Boundaries

In future milestones, the prompt transformation flow will be executed by specialized agents with clear inputs, outputs, and termination conditions:

1. **Requirement Analyzer**:
   - Parses Thai requirements, isolates key features, identifies ambiguities, and flags missing constraints.
2. **Engineering Translator**:
   - Bridges informal Thai terminology to standard software engineering idioms and patterns.
3. **Prompt Architect**:
   - Structures the prompt into standard sections: Context, Instructions, Constraints, Specifications, and Verification.
4. **Prompt Reviewer**:
   - Evaluates prompt completeness, testability, and clarity before presenting to the user.

---

## 3. Knowledge Grounding & RAG Strategy (Milestone 5)

- **Introduction**: Knowledge retrieval will be introduced in **Milestone 5 (Knowledge / RAG)**.
- **Vector Database**: **Qdrant** will be utilized for indexing curated prompt templates and software engineering best practices.
- **Contract Boundary**: In Milestone 1, `BaseKnowledgeRetriever` in `app/rag/base.py` establishes the abstract interface without requiring Qdrant or Docker.
