# Infrastructure

## Desktop-First Local Architecture

The **AI Engineering Assistant** is designed as a desktop-first application.

- **Primary Database**: Embedded SQLite (`data/app.db`), requiring no external database server, no background services, and zero Docker configuration for standard local operation.
- **Future Vector Database (M5)**: Qdrant will be introduced in Milestone 5 (Knowledge / RAG) as a sidecar or optional container.
