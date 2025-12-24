from types import SimpleNamespace
from ConcertScheduleBot.__main__ import get_user_id


def test_get_user_id_from_user():
    msg = SimpleNamespace(
        from_user=SimpleNamespace(id=123), chat=SimpleNamespace(id=999)
    )
    assert get_user_id(msg) == 123


def test_get_user_id_from_chat():
    msg = SimpleNamespace(from_user=None, chat=SimpleNamespace(id=999))
    assert get_user_id(msg) == 999
