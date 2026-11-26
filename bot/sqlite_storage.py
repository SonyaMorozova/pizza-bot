import sqlite3
from contextlib import closing
from pathlib import Path

from bot.storage import Storage, default_state


class SQLiteStorage(Storage):

    def __init__(self, db_path: str = "data/users.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    current_state TEXT DEFAULT 'waiting_for_recipe',
                    recipe TEXT,
                    size TEXT,
                    drink TEXT
                )
            """)

    def persist_user(self, user: dict) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute("""
                INSERT INTO users (
                    user_id, username, first_name, last_name
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                user["id"],
                user.get("username"),
                user.get("first_name"),
                user.get("last_name"),
            ))

    def get_user_state(self, user_id: int) -> dict:
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            row = conn.execute("""
                SELECT current_state, recipe, size, drink
                FROM users
                WHERE user_id = ?
            """, (user_id,)).fetchone()

        if row is None:
            return default_state()

        return {
            "current_state": row[0],
            "order_content": {
                "recipe": row[1],
                "size": row[2],
                "drink": row[3],
            },
        }

    def save_user_state(self, user_id: int, state: dict) -> None:
        order = state["order_content"]

        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute("""
                UPDATE users
                SET current_state = ?,
                    recipe = ?,
                    size = ?,
                    drink = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (
                state["current_state"],
                order["recipe"],
                order["size"],
                order["drink"],
                user_id,
            ))