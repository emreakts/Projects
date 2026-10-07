"""Kullanıcı ilerlemesini SQLite'ta saklar."""

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

    def reset(self, user_id: int) -> None:
        self._conn.execute("DELETE FROM progress WHERE user_id = ?", (user_id,))
        self._conn.commit()
