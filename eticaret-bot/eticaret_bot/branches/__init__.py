"""Dropshipping dalları. Her dal kendi yol haritası, ürün kriterleri ve araçlarıyla gelir."""

from ..core.branch import Branch
from ..core.roadmap import task_ids
from . import eihracat, global_ds, yurtici

BRANCHES: dict[str, Branch] = {b.id: b for b in (yurtici.BRANCH, eihracat.BRANCH, global_ds.BRANCH)}

ALL_TASK_IDS = frozenset(tid for b in BRANCHES.values() for tid in task_ids(b.stages))


def branch_of_task(task_id: str) -> Branch:
    return BRANCHES[task_id.split(".", 1)[0]]
