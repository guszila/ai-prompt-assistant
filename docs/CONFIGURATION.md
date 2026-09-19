# Configuration & Security Guide

This document describes how to configure the **AI Engineering Assistant** application, with a focus on LLM provider settings and the desktop security model.

---

## 1. Environment Configuration

The backend AI service loads its configuration from environment variables and an optional `.env` file located in the repository root.

A template is provided in [`.env.example`](file:///d:/Dev/Project/ai-prompt-assistant/ai-prompt-assistant/.env.example).

### Key Configuration Variables

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `AI_SERVICE_HOST` | `str` | `127.0.0.1` | Local loopback host for AI Service backend. |
| `AI_SERVICE_PORT` | `int` | `8000` | Port for the AI Service. |
| `AI_SERVICE_ENV` | `str` | `development` | Environment mode (`development`, `production`). |
| `SQLITE_DB_PATH` | `str` | `data/app.db` | Path to local embedded SQLite database. |
| `LLM_ENABLED` | `bool` | `false` | Enable/disable optional LLM enhancement layer. |
| `LLM_PROVIDER` | `str` | `mock` | Active provider: `mock` (offline/test) or `openai`. |
| `LLM_MODEL` | `str` | `gpt-4o-mini` | Model identifier for OpenAI-compatible endpoint. |
| `LLM_API_KEY` | `SecretStr`| `None` | API key for the LLM provider (masked in logs/repr). |
| `LLM_BASE_URL` | `str` | `None` | Optional custom base URL for OpenAI-compatible endpoints. |
| `LLM_TIMEOUT_SECONDS`| `float` | `15.0` | Maximum request timeout before triggering fallback. |
| `LLM_MAX_RETRIES` | `int` | `2` | Bounded retries for transient network/rate-limit errors. |

---

## 2. Desktop Security & BYOK Model

The AI Engineering Assistant is a desktop-first tool running locally on the user's personal machine. Under this **Bring-Your-Own-Key (BYOK)** model:

### Internal Safeguards
1. **Secret Masking (`pydantic.SecretStr`)**:
   - `LLM_API_KEY` is loaded as a `SecretStr`.
   - Calling `str(settings.LLM_API_KEY)` or `repr(settings.LLM_API_KEY)` returns `**********`.
   - Access to the raw key is restricted exclusively to provider client initialization via `.get_secret_value()`.
2. **Log & Trace Sanitization**:
   - HTTP request headers (`Authorization: Bearer ...`) and exception messages are strictly redacted to prevent API keys from appearing in logs or error traces.
3. **Frontend Isolation**:
   - API keys are **never** bundled, sent to, or stored in the frontend Svelte/Tauri application.
   - The desktop frontend communicates solely via local loopback HTTP (`127.0.0.1:8000`).

### Realistic Desktop Security Limitation
> [!WARNING]
> While `SecretStr` prevents in-app leaks and log exposure, any secret stored in a local `.env` file or local process memory is accessible to other processes running under the same user OS account. In future milestones, encrypted OS keychain integration will be explored.
