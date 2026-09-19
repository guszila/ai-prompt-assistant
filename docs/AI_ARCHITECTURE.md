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

---

## 4. Core Prompt Engine Pipeline (Milestone 2)

Milestone 2 establishes a deterministic, LLM-independent prompt engine that transforms raw natural language requirements into structured engineering prompts without requiring external models or network access.

```text
PromptRequest
    │
    ▼
RequirementNormalizer       (Collapses whitespace, Unicode normalization, language detection)
    │
    ▼
RequirementAnalyzer         (Extracts actions, entities, explicit constraints)
    │
    ├── EngineeringTerminologyMapper (AuthN != AuthZ, generic API != RESTful API, inferred concepts tagged)
    ├── AmbiguityDetector            (Identifies missing functional operations; avoids tech stack demands)
    │
    ▼
PromptComposer              (Assembles standardized Markdown; omits empty sections; formalizes acceptance criteria)
    │
    ▼
PromptValidator             (Ensures completeness, verifies question coverage, blocks fabricated performance metrics)
    │
    ▼
PromptTransformationResponse
```

### Architectural Guarantees
1. **Zero Requirement Fabrication**: The engine never invents unrequested technical constraints or arbitrary performance metrics (e.g. latency, throughput).
2. **Strict Concept Separation**: Authentication (login, credentials) is strictly distinct from Authorization (roles, permissions). Generic "API" is never conflated with "RESTful API".
3. **Explicit Assumptions**: Any inferred technical capability is tagged with `is_inferred = True` and surfaced as an explicit `Assumption` requiring user confirmation.
4. **Deterministic Reproducibility**: Identical input text and configuration produce bit-for-bit identical markdown and structural analysis.

---

## 5. LLM Integration Layer & Grounding Architecture (Milestone 3)

Milestone 3 introduces an optional, provider-agnostic **LLM Integration Layer** that enhances requirement understanding and prompt vocabulary without compromising the deterministic M2 baseline.

### 5.1 Architecture & Pipeline Preservation

```text
                         User Requirement
                                │
                                ▼
                     ┌────────────────────┐
                     │ M2 Normalizer      │  (Preserves original text, Unicode cleaning)
                     └─────────┬──────────┘
                               ▼
                     ┌────────────────────┐
                     │ M2 Analyzer        │  (Extracts entities, actions, explicit constraints;
                     │  ├── Terminology   │   AuthN != AuthZ, generic API != RESTful API;
                     │  │   Mapper        │   Functional ambiguity detection)
                     │  └── Ambiguity     │
                     │      Detector      │
                     └─────────┬──────────┘
                               ▼
                     ┌────────────────────┐
                     │ M2 Baseline        │  (Authoritative Ground Truth Baseline)
                     │ RequirementAnalysis│
                     └─────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ (If LLM disabled)   │ (If LLM enabled)
                    │                     ▼
                    │            ┌────────────────────┐
                    │            │ LLM Provider       │  (Receives User Text + M2 Baseline)
                    │            └─────────┬──────────┘
                    │                      ▼
                    │            ┌────────────────────┐
                    │            │ LLMRequirement     │  (Untrusted Candidate Model)
                    │            │ Candidate          │
                    │            └─────────┬──────────┘
                    │                      │
                    └──────────┬───────────┘
                               ▼
                    ┌────────────────────┐
                    │ Grounding          │  (Level 1: Explicit User Input
                    │ Reconciler         │   > Level 2: M2 Deterministic Baseline
                    └─────────┬──────────┘   > Level 3: LLM Candidate)
                              ▼
                     Grounded Requirement
                          Analysis
                              │
                              ▼
                    ┌────────────────────┐
                    │ Prompt Composer    │  (Deterministic Markdown Assembly)
                    └─────────┬──────────┘
                              ▼
                    ┌────────────────────┐
                    │ Prompt Validator   │  (Integrity & Anti-Fabrication Check)
                    └─────────┬──────────┘
                              ▼
                     Final Engineering
                           Prompt
```

### 5.2 Grounding & Reconciliation Guarantees
1. **Explicit Priority Order**:
   - **Level 1 (Explicit User Input)**: Cannot be contradicted, overridden, or deleted by the LLM.
   - **Level 2 (M2 Deterministic Analysis)**: Authoritative baseline for concept mapping.
   - **Level 3 (LLM Candidate)**: Untrusted suggestions. May enrich vocabulary, suggest clarifications, or propose architectural assumptions.
2. **Strict Category Distinction**:
   - Explicit Requirements (user commanded).
   - Inferred Concepts (rule-based M2 mappings).
   - Assumptions (unconfirmed model inferences requiring user review).
   - Clarifications (targeted functional questions).
3. **Anti-Hallucination Boundaries**:
   - Login input will **never** generate confirmed Authorization/RBAC requirements unless explicitly commanded.
   - Generic "API" input will **never** generate confirmed RESTful API requirements unless explicitly commanded.
   - Speculative databases (PostgreSQL, Redis, MongoDB) and performance numbers (<500ms, 99.9%) are strictly blocked from entering requirements and acceptance criteria.

### 5.3 Failure Isolation & Graceful Degradation
Failures originating from the optional LLM enhancement layer (network drop, timeout, 401, 429, schema validation) do not break the core prompt transformation pipeline. The system catches the error, sets a typed failure reason (`LLMFallbackReason`), and immediately falls back to the authoritative M2 baseline analysis.


