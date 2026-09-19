import tempfile
from pathlib import Path
from app.repositories.base import IRepository
from app.repositories.sqlite_repo import SQLiteRepository


def test_sqlite_repository_is_irepository_instance():
    """Verify that SQLiteRepository satisfies the IRepository contract."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        repo = SQLiteRepository(db_path=db_file)
        assert isinstance(repo, IRepository)


def test_sqlite_repository_crud_operations():
    """Test create, read, update, delete, and list operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test.db"
        repo = SQLiteRepository(db_path=db_file)

        # 1. Non-existent item
        assert repo.get("non-existent") is None

        # 2. Create / Save item
        payload = {"key": "test_1", "value": "Initial value", "active": True}
        repo.save("item_1", payload)

        # 3. Read item
        item = repo.get("item_1")
        assert item is not None
        assert item["key"] == "test_1"
        assert item["value"] == "Initial value"
        assert item["active"] is True

        # 4. Update item
        updated_payload = {"key": "test_1", "value": "Updated value", "active": False}
        repo.save("item_1", updated_payload)
        updated_item = repo.get("item_1")
        assert updated_item is not None
        assert updated_item["value"] == "Updated value"

        # 5. List items
        repo.save("item_2", {"key": "test_2", "value": "Second"})
        all_items = repo.list_all()
        assert len(all_items) == 2

        # 6. Delete item
        deleted = repo.delete("item_1")
        assert deleted is True
        assert repo.get("item_1") is None
        assert len(repo.list_all()) == 1


def test_sqlite_persistence_across_connections():
    """Verify that data written in one connection is persisted and readable from an independent connection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "persisted.db"

        # Connection 1: Write data
        repo_write = SQLiteRepository(db_path=db_file)
        repo_write.save("persist_id", {"status": "persisted", "counter": 42})
        del repo_write

        # Connection 2: Open new connection to same database file and verify data
        repo_read = SQLiteRepository(db_path=db_file)
        retrieved = repo_read.get("persist_id")
        assert retrieved is not None
        assert retrieved["status"] == "persisted"
        assert retrieved["counter"] == 42


def test_sqlite_parameterized_queries_safety():
    """Verify that inputs with special characters/SQL fragments are safely handled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "safety.db"
        repo = SQLiteRepository(db_path=db_file)

        dangerous_id = "test' OR '1'='1"
        dangerous_payload = {"text": "hello'; DROP TABLE kv_store; --"}

        repo.save(dangerous_id, dangerous_payload)
        retrieved = repo.get(dangerous_id)
        assert retrieved is not None
        assert retrieved["text"] == dangerous_payload["text"]

        # Verify table still exists and only 1 record exists
        all_records = repo.list_all()
        assert len(all_records) == 1
