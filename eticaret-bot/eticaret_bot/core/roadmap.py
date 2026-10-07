"""Yol haritası motoru: aşamalar, görevler ve ilerleme hesapları (dallardan bağımsız)."""

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    text: str


@dataclass(frozen=True)
class Stage:
    id: str  # "<dal>.<aşama>", ör. "c.sirket"
    title: str
    guide: str
    tasks: tuple[Task, ...]


def make_stage(branch_id: str, key: str, title: str, guide: str, tasks: list[str]) -> Stage:
    sid = f"{branch_id}.{key}"
    return Stage(sid, title, guide, tuple(Task(f"{sid}.{i}", t) for i, t in enumerate(tasks, 1)))


def task_ids(stages: Sequence[Stage]) -> tuple[str, ...]:
    return tuple(t.id for s in stages for t in s.tasks)


def find_stage(stages: Sequence[Stage], stage_id: str) -> Stage:
    for s in stages:
        if s.id == stage_id:
            return s
    raise KeyError(stage_id)


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
