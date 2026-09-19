# Data Model Specification

## 1. Core Domain Entities (Contracts)

In Milestone 1, domain models exist as lightweight data transfer contracts (Pydantic v2 and TypeScript interfaces) without premature database table binding:

```text
PromptRequest ──(1:1)──> PromptAnalysis ──(1:N)──> EngineeringPrompt
                                                        │
                                                        ├──(1:N)──> PromptFeedback
                                                        └──(1:1)──> Experience
```

---

## 2. Entity Contracts

### PromptRequest
- `id` (String / UUID): Unique request identifier.
- `raw_text` (String): Original user input in Thai.
- `language` (Enum: `th`, `en`): Input language.
- `project_context_id` (String, Optional): Associated project conventions.
- `metadata` (Dictionary, Optional): Contextual metadata.
- `created_at` (Timestamp): Request creation time.

### PromptAnalysis
- `request_id` (String): Reference to `PromptRequest`.
- `identified_intent` (String): Extracted engineering goal.
- `technical_domain` (String): Backend, Frontend, DevOps, etc.
- `ambiguities` (Array[String]): Missing constraints or ambiguities.
- `extracted_constraints` (Array[String]): Concrete constraints.
- `assumptions` (Array[String]): Explicit assumptions made.
- `suggested_clarifications` (Array[String]): Clarifications needed.

### EngineeringPrompt
- `id` (String / UUID): Unique prompt identifier.
- `request_id` (String): Reference to `PromptRequest`.
- `title` (String): Concise task title.
- `system_context` (String): Background context.
- `role_definition` (String): Target persona (e.g. Senior Backend Engineer).
- `task_instructions` (String): Concrete execution steps.
- `technical_constraints` (Array[String]): Guardrails and conventions.
- `input_output_specification` (String): Precise contracts.
- `verification_steps` (Array[String]): Testing and validation instructions.
- `version` (Integer): Incremental revision number.
- `status` (Enum): `draft`, `analyzed`, `generated`, `reviewed`, `approved`, `rejected`.

### PromptFeedback
- `id` (String / UUID): Unique feedback identifier.
- `prompt_id` (String): Reference to `EngineeringPrompt`.
- `rating` (Integer, 1-5): User satisfaction score.
- `user_comment` (String, Optional): Qualitative feedback.
- `revised_prompt_content` (String, Optional): Manual modifications.
- `is_accepted` (Boolean): Explicit user approval flag.

---

## 3. Storage Strategy

- **Milestone 1 (Foundation)**:
  - Local embedded **SQLite** database (`data/app.db`).
  - Standard library `sqlite3` with generic repository boundary (`IRepository[T]`).
  - No ORM, no complex migration framework, no premature table creation for all entities.
- **Milestone 5 (Knowledge / RAG)**:
  - **Qdrant** vector store introduced for semantic prompt templates and technical knowledge grounding.
