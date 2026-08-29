"""Small, private-by-default SQLite conversation store.

Ankiy deliberately keeps only recent messages in prompts. The complete local transcript
remains in `data/ankiy.sqlite3`, which is ignored by git and can be deleted at any time.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


Role = Literal["user", "assistant"]


@dataclass(frozen=True, slots=True)
class Message:
    role: Role
    content: str


class MemoryStore:
    """A minimal synchronous SQLite store; safe to use from one bot process."""

    def __init__(self, database_path: Path):
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                PRAGMA journal_mode = WAL;
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    profile_key TEXT NOT NULL,
                    voice_enabled INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
                );
                CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
                    ON messages(conversation_id, id);
                """
            )

    def ensure_conversation(self, conversation_id: str, profile_key: str) -> str:
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO conversations (id, profile_key) VALUES (?, ?)
                ON CONFLICT(id) DO NOTHING
                """,
                (conversation_id, profile_key),
            )
            row = db.execute(
                "SELECT profile_key FROM conversations WHERE id = ?", (conversation_id,)
            ).fetchone()
        assert row is not None
        return str(row["profile_key"])

    def profile_for(self, conversation_id: str, fallback: str) -> str:
        return self.ensure_conversation(conversation_id, fallback)

    def switch_profile(self, conversation_id: str, profile_key: str) -> None:
        """Switch profiles and start their chat with a clean contextual slate."""
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO conversations (id, profile_key) VALUES (?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    profile_key = excluded.profile_key,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (conversation_id, profile_key),
            )
            db.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))

    def append(self, conversation_id: str, role: Role, content: str) -> None:
        if role not in ("user", "assistant"):
            raise ValueError(f"Unsupported message role: {role}")
        clean = content.strip()
        if not clean:
            return
        with self._connect() as db:
            db.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, clean),
            )
            db.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conversation_id,),
            )

    def recent(self, conversation_id: str, limit: int = 16) -> list[Message]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT role, content FROM (
                    SELECT id, role, content FROM messages
                    WHERE conversation_id = ?
                    ORDER BY id DESC LIMIT ?
                ) ORDER BY id ASC
                """,
                (conversation_id, limit),
            ).fetchall()
        return [Message(role=row["role"], content=row["content"]) for row in rows]

    def clear(self, conversation_id: str) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            db.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conversation_id,),
            )

    def voice_enabled(self, conversation_id: str, fallback_profile: str) -> bool:
        self.ensure_conversation(conversation_id, fallback_profile)
        with self._connect() as db:
            row = db.execute(
                "SELECT voice_enabled FROM conversations WHERE id = ?", (conversation_id,)
            ).fetchone()
        return bool(row and row["voice_enabled"])

    def set_voice_enabled(
        self, conversation_id: str, fallback_profile: str, enabled: bool
    ) -> None:
        self.ensure_conversation(conversation_id, fallback_profile)
        with self._connect() as db:
            db.execute(
                "UPDATE conversations SET voice_enabled = ? WHERE id = ?",
                (int(enabled), conversation_id),
            )
