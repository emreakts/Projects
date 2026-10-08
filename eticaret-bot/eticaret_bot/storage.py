"""Kullanıcı ilerlemesini SQLite'ta saklar."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Storage:
    def __init__(self, path: str | Path):
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS progress ("
            " user_id INTEGER NOT NULL,"
            " task_id TEXT NOT NULL,"
            " PRIMARY KEY (user_id, task_id))"
        )
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS profile (user_id INTEGER PRIMARY KEY, branch TEXT NOT NULL)"
        )
        self._conn.commit()

    def done_tasks(self, user_id: int) -> set[str]:
        rows = self._conn.execute("SELECT task_id FROM progress WHERE user_id = ?", (user_id,))
        return {r[0] for r in rows}

    def toggle_task(self, user_id: int, task_id: str) -> bool:
        """Görevi işaretler/işareti kaldırır. Yeni durum tamamlandıysa True döner."""
        cur = self._conn.execute(
            "DELETE FROM progress WHERE user_id = ? AND task_id = ?", (user_id, task_id)
        )
        if cur.rowcount == 0:
            self._conn.execute(
                "INSERT INTO progress (user_id, task_id) VALUES (?, ?)", (user_id, task_id)
            )
        self._conn.commit()
        return cur.rowcount == 0

    def mark_done(self, user_id: int, task_id: str) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO progress (user_id, task_id) VALUES (?, ?)", (user_id, task_id)
        )
        self._conn.commit()

    def get_branch(self, user_id: int) -> str | None:
        row = self._conn.execute("SELECT branch FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        return row[0] if row else None

    def set_branch(self, user_id: int, branch: str) -> None:
        self._conn.execute(
            "INSERT INTO profile (user_id, branch) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET branch = excluded.branch",
            (user_id, branch),
        )
        self._conn.commit()

    def reset(self, user_id: int) -> None:
        """İlerlemeyi ve seçili modeli siler (kullanıcı baştan başlar)."""
        self._conn.execute("DELETE FROM progress WHERE user_id = ?", (user_id,))
        self._conn.execute("DELETE FROM profile WHERE user_id = ?", (user_id,))
        self._conn.commit()
