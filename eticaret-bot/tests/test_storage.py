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
