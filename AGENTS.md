# AGENTS.md

# AI Engineering Assistant — Agent Rules

This document defines the mandatory rules for AI coding agents working on this repository.

The purpose of this file is to ensure that the project remains maintainable, testable, secure, modular, and recoverable as the codebase grows.

---

# 1. Project Overview

This repository contains a desktop application called:

**AI Engineering Assistant**

The primary purpose of the application is to transform natural-language Thai requirements into precise, structured English prompts optimized for software engineering and AI coding agents.

The long-term vision is to build a continuously improving AI engineering system that can:

- Understand Thai software requirements.
- Extract technical intent.
- Identify ambiguity.
- Transform natural language into software engineering terminology.
- Generate structured engineering prompts.
- Validate prompt quality.
- Retrieve relevant technical knowledge.
- Use specialized AI agents.
- Collect user feedback and corrections.
- Build high-quality training datasets.
- Evaluate model performance.
- Support fine-tuning and model versioning.
- Eventually support local/open-weight models.

The system must be designed for long-term extensibility.

---

# 2. Core Engineering Principles

Always prioritize the following order:

1. Correctness
2. Security
3. Maintainability
4. Testability
5. Modularity
6. Extensibility
7. Performance
8. User experience
9. Visual appearance

Do not sacrifice architecture quality for visual complexity.

The application is an engineering tool.

The quality of the underlying system is more important than visual effects.

---

# 3. Technology Architecture

The intended architecture is:

```text
Desktop Application
    │
    ├── Tauri 2
    │
    ├── Svelte 5
    │
    └── TypeScript
            │
            ▼
       AI Service
            │
            └── Python + FastAPI
                    │
                    ├── AI Agents
                    ├── Prompt Engine
                    ├── LLM Providers
                    ├── RAG
                    └── Evaluation
                            │
                            ├── PostgreSQL
                            └── Qdrant
```

Primary technologies:

- Tauri 2
- Rust
- Svelte 5
- TypeScript
- Python
- FastAPI
- PostgreSQL
- Qdrant
- Docker
- Git

Additional technologies must have a clear technical justification.

Do not introduce dependencies simply because they are popular.

---

# 4. Repository Structure

The repository should generally follow this structure:

```text
ai-engineering-assistant/

├── apps/
│   ├── desktop/
│   └── ai-service/
│
├── packages/
│   ├── shared-types/
│   ├── prompt-engine/
│   └── schemas/
│
├── infrastructure/
│   ├── docker/
│   ├── postgres/
│   └── qdrant/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── datasets/
│   └── evaluation/
│
├── docs/
│
├── scripts/
│
├── tests/
│
├── AGENTS.md
├── README.md
├── .env.example
└── .gitignore
```

Do not reorganize the repository without a clear architectural reason.

If a structural change is necessary, explain the reason before making a major change.

---

# 5. Separation of Responsibilities

Maintain strict separation between:

- UI
- Application logic
- Domain logic
- AI orchestration
- LLM providers
- Data access
- Knowledge retrieval
- Evaluation
- Training

Do not place business logic directly inside UI components.

Do not place database logic directly inside UI components.

Do not place LLM provider calls directly inside UI components.

Use appropriate service, domain, and repository boundaries.

---

# 6. Frontend Rules

The desktop frontend uses:

- Svelte 5
- TypeScript
- Tauri

Frontend responsibilities include:

- user interaction
- displaying application state
- input/output interfaces
- prompt editing
- project configuration
- feedback collection

Frontend should NOT directly implement:

- database access
- model training
- complex AI orchestration
- provider-specific LLM logic

Keep components focused and reusable.

Prefer feature-oriented organization over large generic component folders when appropriate.

---

# 7. TypeScript Rules

Use strict TypeScript.

Avoid:

```ts
any
```

unless there is a documented technical reason.

Prefer explicit types.

Use interfaces or appropriate type definitions for system boundaries.

Do not duplicate the same type definition across multiple packages.

Shared domain types should have a single source of truth.

Avoid unnecessary type casting.

Do not silence TypeScript errors without understanding the underlying issue.

---

# 8. Python Rules

Use Python for AI/ML and AI service responsibilities.

Use:

- type hints
- clear modules
- explicit error handling
- isolated business logic
- testable services

Avoid putting all functionality into a single file.

Do not create unnecessary global state.

Keep provider-specific implementation behind appropriate abstractions.

---

# 9. AI Architecture Rules

The AI system must be modular.

Potential agents include:

```text
Requirement Analyzer
Engineering Translator
Prompt Architect
Prompt Reviewer
```

Each agent must have a clear responsibility.

Do not create an agent simply because multiple prompts can be placed into separate files.

Use agents when separation provides a meaningful architectural benefit.

Avoid uncontrolled autonomous agent loops.

Any multi-agent workflow must have:

- clear inputs
- clear outputs
- defined responsibilities
- termination conditions
- error handling

---

# 10. LLM Provider Abstraction

Never tightly couple the application to one LLM provider.

Use an abstraction such as:

```text
LLMProvider
```

The architecture should allow multiple implementations.

For example:

```text
LLMProvider
├── CloudProviderA
├── CloudProviderB
└── LocalModelProvider
```

Do not place provider-specific API calls throughout the application.

Provider-specific code belongs inside the provider integration layer.

Never hard-code:

- API keys
- secrets
- tokens
- credentials

---

# 11. Prompt Engineering Rules

The application is not a simple translation system.

The system should distinguish between:

```text
Natural Language
        ↓
Intent
        ↓
Requirements
        ↓
Technical Context
        ↓
Constraints
        ↓
Engineering Prompt
```

Do not perform literal translation when a technical interpretation is more appropriate.

However:

**Never invent requirements that the user did not provide.**

If a missing requirement materially affects implementation, identify the ambiguity and request clarification or explicitly mark the assumption.

---

# 12. Prompt Quality

Generated prompts should prioritize:

- clarity
- correctness
- technical precision
- actionable instructions
- appropriate context
- explicit constraints
- testability

Do not make prompts unnecessarily long.

More text does not automatically mean a better prompt.

---

# 13. Database Rules

PostgreSQL is the primary structured database.

Qdrant is the vector/semantic retrieval system.

Do not access either database directly from UI components.

Use repository or service boundaries.

Database schema changes must be deliberate.

Do not modify existing database structures without checking their dependencies.

Never delete production-like data as part of normal development without explicit authorization.

---

# 14. Data and Learning Rules

The application is intended to support continuous improvement.

User interactions may eventually produce:

```text
Input
↓
Generated Output
↓
User Edit
↓
Feedback
↓
Evaluation
↓
Training Example
```

However:

**Do not automatically train a model on every interaction.**

Every interaction may be collected as experience data, but training data must pass quality control.

Potential data-quality stages:

```text
Raw Experience
↓
Validation
↓
Deduplication
↓
Quality Filtering
↓
Evaluation
↓
Training Dataset
```

Never assume user edits are automatically correct.

---

# 15. Privacy and Security

Treat user prompts, project information, source code, and feedback as potentially sensitive.

Do not expose data unnecessarily.

Do not send data to an external provider unless the configured workflow requires it.

Do not log secrets.

Do not log API keys.

Do not store credentials in source control.

Use environment variables or secure credential storage.

The `.env` file must never be committed.

Maintain `.env.example` with placeholder values.

---

# 16. Error Handling

Errors must be handled explicitly.

Do not silently ignore failures.

Errors should provide enough information for debugging without exposing secrets.

For external services, account for:

- network failures
- timeout
- rate limits
- invalid responses
- authentication errors
- malformed data

AI-generated output should also be validated before being treated as trusted application data.

---

# 17. Testing Rules

Testing is mandatory for important functionality.

At minimum, support:

- unit tests
- integration tests
- API tests
- prompt-engine tests
- AI evaluation tests
- regression tests

Core business logic should be testable without requiring the full desktop application.

Do not rely exclusively on manual testing.

For AI functionality, maintain evaluation examples that can be used to detect regressions between model or prompt-engine versions.

---

# 18. Git Rules

Git is mandatory.

The repository must always remain recoverable to a known-good state.

Before starting work:

```bash
git status
```

Check whether the working tree contains existing user changes.

Never overwrite user changes.

Never assume the working tree is clean.

---

# 19. Commit Strategy

Create a commit after completing a meaningful feature or milestone.

Do NOT create a commit for every individual file.

A commit should represent a coherent and verified state.

Examples:

```text
chore: initialize project structure
feat: add desktop application shell
feat: add prompt input
feat: add requirement analyzer
feat: add prompt generation
feat: add prompt validation
test: add prompt engine tests
refactor: separate llm provider abstraction
```

Use Conventional Commits where practical.

---

# 20. Before Committing

Before creating a commit:

1. Check Git status.
2. Review changed files.
3. Run relevant tests.
4. Run type checking.
5. Run linting.
6. Verify the feature.
7. Confirm no secrets are included.
8. Confirm no unrelated files were changed.

Only commit a known-good state.

---

# 21. Rollback Safety

Git must always allow recovery to a previous known-good state.

Do not use destructive commands such as:

```bash
git reset --hard
git clean -fd
```

unless the user explicitly authorizes the operation.

Do not delete or overwrite user changes.

If a feature causes significant problems:

1. Stop.
2. Inspect the current state.
3. Identify the last known-good commit.
4. Explain the problem.
5. Recommend a recovery approach.
6. Wait for authorization before destructive rollback operations.

Prefer fixing forward when practical.

---

# 22. Feature Development Workflow

Every feature should generally follow:

```text
Understand
    ↓
Inspect existing code
    ↓
Plan
    ↓
Implement
    ↓
Test
    ↓
Review
    ↓
Verify
    ↓
Commit
```

Do not immediately start editing files without understanding the existing architecture.

Before modifying an existing feature, inspect:

- related files
- dependencies
- tests
- interfaces
- recent Git history

---

# 23. Change Scope

When implementing a feature:

- Modify only necessary files.
- Avoid unrelated refactoring.
- Avoid changing public interfaces without justification.
- Avoid introducing dependencies unnecessarily.
- Preserve existing behavior unless the feature explicitly changes it.

If a refactor is necessary, explain why.

---

# 24. Dependency Rules

Before adding a dependency, consider:

1. Is it necessary?
2. Can the requirement be implemented using existing dependencies?
3. Is the project actively maintained?
4. Does it introduce security or licensing concerns?
5. Does it significantly increase complexity?

Do not add dependencies simply for convenience.

---

# 25. Documentation Rules

Update documentation when architecture or behavior changes significantly.

Important documentation includes:

```text
README.md
docs/ARCHITECTURE.md
docs/REQUIREMENTS.md
docs/DATA_MODEL.md
docs/AI_ARCHITECTURE.md
docs/ROADMAP.md
AGENTS.md
```

Do not allow documentation to describe an architecture that no longer exists.

---

# 26. AI Coding Agent Behavior

When working on this repository, act as a senior software engineer.

Before making changes:

1. Read `AGENTS.md`.
2. Inspect the relevant project structure.
3. Inspect related source files.
4. Check Git status.
5. Understand existing interfaces and dependencies.

Do not assume the current implementation matches your expectations.

Use the existing architecture unless there is a justified reason to change it.

---

# 27. Do Not Over-Engineer

This project is intended to grow significantly, but future requirements must not be implemented prematurely.

Do not create:

- unnecessary abstractions
- unused interfaces
- unused services
- speculative infrastructure
- unnecessary microservices
- unnecessary agents

Design for extensibility, but implement only what the current milestone requires.

---

# 28. Working With Existing Code

Before modifying existing code:

- understand what it does
- identify its callers
- inspect related tests
- preserve backward compatibility where possible

Do not rewrite an entire module when a focused change is sufficient.

Do not replace working code simply because you prefer another style.

---

# 29. Verification

Never claim that a feature is complete merely because code was written.

A feature is complete only after appropriate verification.

When possible, verify:

```text
Build
Type Check
Lint
Unit Tests
Integration Tests
Runtime Behavior
```

Report failures honestly.

Never claim a test passed if it was not actually run.

---

# 30. Communication Rules

When reporting work:

Be concise but technically precise.

Always distinguish between:

- implemented
- tested
- not tested
- known issue
- assumption

If an important requirement is ambiguous, ask for clarification rather than silently inventing behavior.

For major architectural decisions, explain the reasoning.

---

# 31. Definition of Done

A task is considered complete when:

- implementation is complete
- relevant tests pass
- type checks pass
- lint checks pass where applicable
- no unrelated files were modified
- documentation is updated when necessary
- security requirements are satisfied
- Git state is clean or intentionally contains user changes
- a meaningful Git commit is created when the task represents a completed milestone

---

# 32. Golden Rule

When uncertain:

**Do not guess silently.**

Inspect the codebase first.

If the correct behavior cannot be determined from the project requirements, existing implementation, documentation, or tests:

- identify the uncertainty
- explain the options
- ask for clarification when necessary

The goal is not to write the maximum amount of code.

The goal is to build a reliable, maintainable, high-quality engineering system.