import os
from ConcertScheduleBot.__main__ import (
    user_keyboard,
    TOGGLE_OFF_TEXT,
    TOGGLE_ON_TEXT,
)


def test_user_keyboard_with_recs():
    kb = user_keyboard(True)
    assert kb.keyboard[0][0].text == TOGGLE_OFF_TEXT


def test_user_keyboard_without_recs():
    kb = user_keyboard(False)
    assert kb.keyboard[0][0].text == TOGGLE_ON_TEXT
