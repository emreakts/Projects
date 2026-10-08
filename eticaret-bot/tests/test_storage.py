from eticaret_bot.storage import Storage


def test_toggle_and_reset(tmp_path):
    s = Storage(tmp_path / "t.db")
    assert s.toggle_task(1, "model.1") is True
    assert s.done_tasks(1) == {"model.1"}
    assert s.done_tasks(2) == set()
    assert s.toggle_task(1, "model.1") is False
    assert s.done_tasks(1) == set()
    s.toggle_task(1, "urun.2")
    s.reset(1)
    assert s.done_tasks(1) == set()


def test_profile_branch_and_reset(tmp_path):
    s = Storage(tmp_path / "t.db")
    assert s.get_branch(1) is None
    s.set_branch(1, "a")
    s.set_branch(1, "c")
    assert s.get_branch(1) == "c"
    assert s.get_branch(2) is None
    s.mark_done(1, "c.pazar.1")
    s.mark_done(1, "c.pazar.1")
    assert s.done_tasks(1) == {"c.pazar.1"}
    s.reset(1)
    assert s.get_branch(1) is None and s.done_tasks(1) == set()
