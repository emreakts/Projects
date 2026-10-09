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


@pytest.mark.parametrize("branch", READY, ids=lambda b: b.id)
def test_ready_branch_tasks_all_have_how_to(branch):
    assert all(t.how for s in branch.stages for t in s.tasks)


@pytest.mark.parametrize("branch", READY, ids=lambda b: b.id)
def test_task_views_fit_telegram_limits(branch):
    from eticaret_bot.bot import task_view

    ids = roadmap.task_ids(branch.stages)
    for done in (set(), set(ids)):
        for tid in ids:
            text, markup = task_view(branch, tid, done)
            assert len(text) < 4096
            for row in markup.inline_keyboard:
                for btn in row:
                    assert len(btn.callback_data.encode()) <= 64


def test_task_view_shortcuts_and_navigation():
    from eticaret_bot.bot import task_view

    b = BRANCHES["c"]
    ids = roadmap.task_ids(b.stages)
    first_text, first = task_view(b, ids[0], set())
    data = [btn.callback_data for row in first.inline_keyboard for btn in row]
    assert f"ch:{ids[0]}:us" in data and f"tk:{ids[1]}" in data  # ilk adım bir seçim
    _, plain = task_view(b, "c.pazar.3", set())
    assert "done:c.pazar.3" in [btn.callback_data for row in plain.inline_keyboard for btn in row]
    assert not any(d.startswith("tk:") and d != f"tk:{ids[1]}" for d in data)  # ilk adımda "önceki" yok
    _, kar_task = roadmap.find_task(b.stages, "c.urun.4")
    _, markup = task_view(b, kar_task.id, {kar_task.id})
    data = [btn.callback_data for row in markup.inline_keyboard for btn in row]
    assert "fm:c:kar" in data and f"tg:{kar_task.id}" in data


def test_load_env_file(tmp_path, monkeypatch):
    from eticaret_bot.bot import load_env_file

    env = tmp_path / ".env"
    env.write_text('# yorum\nX_TEST_TOKEN="abc:123"\nX_TEST_DB=a.db\n', encoding="utf-8")
    monkeypatch.delenv("X_TEST_TOKEN", raising=False)
    monkeypatch.setenv("X_TEST_DB", "onceden.db")
    load_env_file(str(env))
    import os

    assert os.environ["X_TEST_TOKEN"] == "abc:123"
    assert os.environ["X_TEST_DB"] == "onceden.db"
    monkeypatch.delenv("X_TEST_TOKEN")


def test_menu_view_with_and_without_branch():
    from eticaret_bot.bot import menu_view

    _, markup = menu_view(None, set())
    data = [b.callback_data for row in markup.inline_keyboard for b in row]
    assert "qz" in data and "models" in data
    b = BRANCHES["c"]
    text, markup = menu_view(b, set())
    data = [b2.callback_data for row in markup.inline_keyboard for b2 in row]
    assert data[0] == "guide:c" and "ps:c" in data and "fm:c:kar" in data and "fm:c:reklam" in data
    assert b.title in text


def test_task_view_header_prefix():
    from eticaret_bot.bot import task_view

    b = BRANCHES["a"]
    first = roadmap.task_ids(b.stages)[0]
    text, _ = task_view(b, first, set(), header="✅ <b>Senin yolun</b>\n")
    assert text.startswith("✅ <b>Senin yolun</b>")
    assert "1." in text  # nasıl yapılır adımları numaralı


@pytest.mark.parametrize("branch", READY, ids=lambda b: b.id)
def test_task_views_with_quiz_header_fit(branch):
    from eticaret_bot.bot import quiz_result, task_view

    # En uzun başlık: en çok aşaması olan dalın sonucu
    _, header = quiz_result("000000" if branch.id == "a" else "222222")
    for tid in roadmap.task_ids(branch.stages):
        text, _ = task_view(branch, tid, set(), header)
        assert len(text) < 4096, tid


def test_branch_a_tasks_are_full_lessons():
    b = BRANCHES["a"]
    tasks = [t for s in b.stages for t in s.tasks]
    assert all(t.how for t in tasks)
    assert all(t.done for t in tasks if not t.options)  # seçenekli adımda seçim = bitti
    assert any(t.template for t in tasks)
    assert sum(bool(t.options) for t in tasks) >= 6


def _all_choice_combos(branch):
    """Her seçenekli görev için her seçeneği tek tek seçili kabul eden senaryolar."""
    yield {}
    for s in branch.stages:
        for t in s.tasks:
            for o in t.options:
                yield {t.id: o.key}


@pytest.mark.parametrize("branch", READY, ids=lambda b: b.id)
def test_option_views_fit_and_buttons_valid(branch):
    from eticaret_bot.bot import quiz_result, task_view

    _, header = quiz_result("000000" if branch.id == "a" else "222222")
    for choices in _all_choice_combos(branch):
        for tid in roadmap.task_ids(branch.stages):
            text, markup = task_view(branch, tid, set(), header, choices)
            assert len(text) < 4096, (tid, choices)
            assert "{secim:" not in text
            for row in markup.inline_keyboard:
                for btn in row:
                    assert len(btn.callback_data.encode()) <= 64
                    assert len(btn.text) <= 64


def test_conditional_options_and_personalization():
    from eticaret_bot.bot import task_view

    b = BRANCHES["a"]
    text, markup = task_view(b, "a.tedarik.1", set(), choices={})
    assert "Petibom" not in text and "Kategorin için" in text
    text, markup = task_view(b, "a.tedarik.1", set(), choices={"a.hazirlik.1": "pet"})
    assert "Petibom" in text and "Evcil hayvan ürünleri için" in text
    data = [btn.callback_data for row in markup.inline_keyboard for btn in row]
    assert "ch:a.tedarik.1:pet1" in data and "done:a.tedarik.1" not in data


def test_option_keys_unique_and_when_refs_valid():
    from eticaret_bot.branches import ALL_TASK_IDS

    for b in READY:
        for s in b.stages:
            for t in s.tasks:
                keys = [o.key for o in t.options]
                assert len(keys) == len(set(keys)), t.id
                for o in t.options:
                    if o.when:
                        dep, key = o.when.split("=")
                        assert dep in ALL_TASK_IDS
                        _, dep_task = roadmap.find_task(b.stages, dep)
                        assert key in {x.key for x in dep_task.options}, (t.id, o.when)


def test_option_task_with_follow_up_action_offers_done_button():
    from eticaret_bot.bot import task_view

    b = BRANCHES["a"]
    text, markup = task_view(b, "a.sirket.1", set(), choices={"a.sirket.1": "online"})
    data = [btn.callback_data for row in markup.inline_keyboard for btn in row]
    assert "<pre>" in text and "Bitti sayılır" in text
    assert "done:a.sirket.1" in data and "ch:a.sirket.1:yerel" in data
    # Saf karar adımında (hazırlık.1) "Yaptım" butonu olmaz; seçim adımı bitirir
    _, markup = task_view(b, "a.hazirlik.1", set(), choices={"a.hazirlik.1": "pet"})
    assert not any(btn.callback_data.startswith("done:") for row in markup.inline_keyboard for btn in row)
