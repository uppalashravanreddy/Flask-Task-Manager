import sqlite3
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from scripts.migrate_add_priority import migrate


@pytest.fixture
def temp_db(tmp_path):
    db_path = str(tmp_path / 'test.db')
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE task (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            desc TEXT NOT NULL
        )
    """)
    conn.execute("INSERT INTO task (title, date, desc) VALUES ('Existing Task', '2026-01-01', 'Old task')")
    conn.commit()
    conn.close()
    return db_path


def test_migration_adds_priority_column(temp_db):
    migrate(db_path=temp_db)
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(task)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    assert 'priority' in columns


def test_migration_backfills_existing_rows_with_medium(temp_db):
    migrate(db_path=temp_db)
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT priority FROM task WHERE title = 'Existing Task'")
    row = cursor.fetchone()
    conn.close()
    assert row[0] == 'Medium'


def test_migration_is_idempotent(temp_db):
    migrate(db_path=temp_db)
    migrate(db_path=temp_db)
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(task)")
    priority_cols = [row for row in cursor.fetchall() if row[1] == 'priority']
    conn.close()
    assert len(priority_cols) == 1


def test_new_rows_after_migration_default_to_medium(temp_db):
    migrate(db_path=temp_db)
    conn = sqlite3.connect(temp_db)
    conn.execute("INSERT INTO task (title, date, desc) VALUES ('New Task', '2026-08-13', 'After migration')")
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("SELECT priority FROM task WHERE title = 'New Task'")
    row = cursor.fetchone()
    conn.close()
    assert row[0] == 'Medium'
