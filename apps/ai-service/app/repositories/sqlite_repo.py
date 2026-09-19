import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional
from app.repositories.base import IRepository


class SQLiteRepository(IRepository[Dict[str, Any]]):
    """
    Intentionally minimal SQLite repository implementation for M1 foundation.
    Uses standard library sqlite3 with parameterized queries and explicit connection lifecycle management.
    """

    def __init__(self, db_path: str | Path = "data/app.db") -> None:
        self.db_path = Path(db_path)
        self._initialize_db()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager that opens, configures, commits, and reliably closes a SQLite connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("PRAGMA journal_mode = WAL;")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _initialize_db(self) -> None:
        """Ensure parent directory exists and minimal table is initialized."""
        if self.db_path.parent:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS kv_store (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def get(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve entity by ID using parameterized query."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT data FROM kv_store WHERE id = ?;", (entity_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row["data"])
            return None

    def save(self, entity_id: str, data: Dict[str, Any]) -> None:
        """Persist or update entity using parameterized query."""
        serialized = json.dumps(data)
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO kv_store (id, data, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                    data = excluded.data,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (entity_id, serialized),
            )

    def delete(self, entity_id: str) -> bool:
        """Delete entity by ID using parameterized query."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM kv_store WHERE id = ?;", (entity_id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        """List all stored entities."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT data FROM kv_store ORDER BY id ASC;")
            return [json.loads(row["data"]) for row in cursor.fetchall()]
