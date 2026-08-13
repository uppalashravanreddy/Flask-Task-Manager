import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'data.db')


def migrate(db_path=None):
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(task)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'priority' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'Medium'")
        cursor.execute("UPDATE task SET priority = 'Medium' WHERE priority IS NULL")
        conn.commit()
        print("Migration complete: 'priority' column added to task table.")
    else:
        print("Migration skipped: 'priority' column already exists.")

    conn.close()


if __name__ == '__main__':
    migrate()
