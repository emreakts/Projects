import pytest

from eticaret_bot.bot import _validate
from eticaret_bot.branches import ALL_TASK_IDS, BRANCHES
from eticaret_bot.core import roadmap

READY = [b for b in BRANCHES.values() if b.ready]


def test_task_ids_unique_and_namespaced():
    ids = [tid for b in BRANCHES.values() for tid in roadmap.task_ids(b.stages)]
    assert len(ids) == len(set(ids)) == len(ALL_TASK_IDS)
    for b in BRANCHES.values():
        assert all(tid.startswith(b.id + ".") for tid in roadmap.task_ids(b.stages))


def test_callback_data_within_telegram_limit():
    # Telegram callback_data en fazla 64 bayt
    for b in BRANCHES.values():
        for tid in roadmap.task_ids(b.stages):
            assert len(f"done:{tid}".encode()) <= 64
        for c in b.criteria:
            assert len(f"pa:{c.key}:5".encode()) <= 64
        for t in b.tools:
            assert len(f"fm:{b.id}:{t.id}".encode()) <= 64


@pytest.mark.parametrize("branch", READY, ids=lambda b: b.id)
def test_ready_branch_has_content(branch):
    assert branch.stages and branch.criteria and branch.tools
    keys = [c.key for c in branch.criteria]
    assert len(keys) == len(set(keys))
    for c in branch.criteria:
        assert all(1 <= s <= 5 for _, s in c.options)
        assert any(s == 1 for _, s in c.options) or not c.hard_flag


@pytest.mark.parametrize(
    "branch,tool", [(b, t) for b in READY for t in b.tools], ids=lambda x: getattr(x, "id", "")
)
def test_tool_report_renders_with_typical_values(branch, tool):
    values = {f.name: f.default if f.default is not None else 50.0 for f in tool.fields}
    text = tool.report(values)
    assert text and "<b>" in text


def test_validate_field_rules():
    from eticaret_bot.core.branch import Field

    assert _validate(Field("x", "?", default=3.5), "-") == 3.5
    with pytest.raises(ValueError):
        _validate(Field("x", "?"), "-")
    with pytest.raises(ValueError):
        _validate(Field("x", "?", kind="positive"), "0")
    with pytest.raises(ValueError):
        _validate(Field("x", "?", kind="pct"), "100")
    assert _validate(Field("x", "?"), "12,5") == 12.5
