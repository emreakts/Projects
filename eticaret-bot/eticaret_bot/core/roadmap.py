"""Yol haritası motoru: aşamalar, görevler ve ilerleme hesapları (dallardan bağımsız)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    text: str
    how: tuple[str, ...] = ()  # "Nasıl yapılır" adımları
    why: str = ""  # neden önemli (tek cümle)
    warn: tuple[str, ...] = ()  # sık yapılan hatalar
    template: str = ""  # kopyalanacak hazır mesaj/metin
    done: str = ""  # adım ne zaman bitmiş sayılır


@dataclass(frozen=True)
class Stage:
    id: str  # "<dal>.<aşama>", ör. "c.sirket"
    title: str
    guide: str
    tasks: tuple[Task, ...]


def make_stage(branch_id: str, key: str, title: str, guide: str, tasks: list) -> Stage:
    """tasks öğeleri: görev metni, (metin, nasıl yapılır adımları) veya
    {"text", "how", "why", "warn", "template", "done"} sözlüğü."""
    sid = f"{branch_id}.{key}"
    built = []
    for i, t in enumerate(tasks, 1):
        tid = f"{sid}.{i}"
        if isinstance(t, str):
            built.append(Task(tid, t))
        elif isinstance(t, dict):
            warn = t.get("warn", ())
            built.append(
                Task(
                    tid,
                    t["text"],
                    how=tuple(t.get("how", ())),
                    why=t.get("why", ""),
                    warn=(warn,) if isinstance(warn, str) else tuple(warn),
                    template=t.get("template", ""),
                    done=t.get("done", ""),
                )
            )
        else:
            text, how = t
            built.append(Task(tid, text, tuple(how)))
    return Stage(sid, title, guide, tuple(built))


def task_ids(stages: Sequence[Stage]) -> tuple[str, ...]:
    return tuple(t.id for s in stages for t in s.tasks)


def find_stage(stages: Sequence[Stage], stage_id: str) -> Stage:
    for s in stages:
        if s.id == stage_id:
            return s
    raise KeyError(stage_id)


def find_task(stages: Sequence[Stage], task_id: str) -> tuple[Stage, Task]:
    for s in stages:
        for t in s.tasks:
            if t.id == task_id:
                return s, t
    raise KeyError(task_id)


def neighbors(stages: Sequence[Stage], task_id: str) -> tuple[str | None, str | None]:
    """Sıralı görev listesinde önceki ve sonraki görevin id'si."""
    ids = task_ids(stages)
    i = ids.index(task_id)
    return (ids[i - 1] if i > 0 else None, ids[i + 1] if i + 1 < len(ids) else None)


def stage_progress(stage: Stage, done: set[str]) -> tuple[int, int]:
    return sum(t.id in done for t in stage.tasks), len(stage.tasks)


def next_task(stages: Sequence[Stage], done: set[str]) -> tuple[Stage, Task] | None:
    """Sırayla ilk tamamlanmamış görevi döndürür; hepsi bittiyse None."""
    for s in stages:
        for t in s.tasks:
            if t.id not in done:
                return s, t
    return None


def progress_bar(done_count: int, total: int, width: int = 10) -> str:
    filled = round(width * done_count / total) if total else 0
    return "▓" * filled + "░" * (width - filled) + f" {done_count}/{total}"
