import itertools
import re

import pytest

from eticaret_bot import academy
from eticaret_bot.bot import lesson_view, quiz_view

ALLOWED_TAGS = {"b", "/b", "i", "/i"}


@pytest.mark.parametrize("n", range(1, len(academy.LESSONS) + 1))
def test_lesson_view_fits_and_is_valid_html(n):
    text, markup = lesson_view(n)
    assert len(text) < 4096
    assert "&" not in text
    tags = re.findall(r"<([^>]*)>", text)
    assert set(tags) <= ALLOWED_TAGS
    assert text.count("<b>") == text.count("</b>") and text.count("<i>") == text.count("</i>")
    data = [b.callback_data for row in markup.inline_keyboard for b in row]
    assert f"lsd:{n}" in data
    assert all(len(d.encode()) <= 64 for d in data)


def test_first_and_last_lesson_navigation():
    _, first = lesson_view(1)
    data = [b.callback_data for row in first.inline_keyboard for b in row]
    assert "ls:2" in data and "ls:0" not in data
    last_n = len(academy.LESSONS)
    text, last = lesson_view(last_n)
    data = [b.callback_data for row in last.inline_keyboard for b in row]
    assert f"ls:{last_n + 1}" not in data
    assert "testi çöz" in " ".join(b.text for row in last.inline_keyboard for b in row)


def test_quiz_questions_and_flow():
    text, markup = quiz_view("")
    assert "Soru 1/" in text
    assert [b.callback_data for b in markup.inline_keyboard[0]] == ["qa:0"]
    text, markup = quiz_view("01")
    assert "Soru 3/" in text
    assert markup.inline_keyboard[0][0].callback_data == "qa:010"


@pytest.mark.parametrize(
    "answers,expected",
    [
        ("000000", "a"),  # düşük bütçe, İngilizce yok, risk istemiyor
        ("222222", "c"),  # yüksek bütçe, iyi İngilizce, reklamla hızlı büyüme
        ("111111", "b"),  # orta yol, döviz hedefi
    ],
)
def test_quiz_recommendations(answers, expected):
    assert academy.recommend(answers)[0] == expected
    text, _ = quiz_view(answers)
    assert "Sonuç" in text


def test_every_answer_combination_renders_result():
    sizes = [range(len(q.options)) for q in academy.QUIZ]
    for combo in itertools.product(*sizes):
        answers = "".join(map(str, combo))
        text, markup = quiz_view(answers)
        assert len(text) < 4096
        assert all(len(b.callback_data.encode()) <= 64 for row in markup.inline_keyboard for b in row)
