from ConcertScheduleBot.__main__ import split_message


def test_split_message_short():
    text = "hello\nworld"
    parts = list(split_message(text, max_len=100))
    assert parts == ["hello\nworld"]


def test_split_message_long():
    text = "a" * 5000
    parts = list(split_message(text, max_len=1000))

    assert len(parts) == 5
    assert all(len(p) <= 1000 for p in parts)
