"""Pytest fixtures for Playwright E2E tests.

Starts the Flask app in a background thread with a temporary SQLite database
so Playwright can hit real HTTP endpoints without needing a separate process.
"""
from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def flask_base_url(tmp_path_factory):
    """Start the Flask app on an ephemeral port, yield the base URL."""
    import sys
    sys.path.insert(0, str(ROOT))

    db_path = tmp_path_factory.mktemp("db") / "test.db"

    import os
    os.environ.setdefault("SECRET_KEY", "playwright-test-secret")

    from app import app, db
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SERVER_NAME"] = None

    with app.app_context():
        db.create_all()

    import socket
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, use_reloader=False),
        daemon=True,
    )
    server_thread.start()
    time.sleep(1.0)

    yield f"http://127.0.0.1:{port}"
