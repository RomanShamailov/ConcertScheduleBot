import pytest
from types import SimpleNamespace
from ConcertScheduleBot.__main__ import toggle_recommendations, get_schedule_maker


@pytest.mark.asyncio
async def test_toggle_recommendations(mocker):
    message = mocker.AsyncMock()
    message.from_user = SimpleNamespace(id=1)
    message.chat = SimpleNamespace(id=1)

    sm = get_schedule_maker(1)
    initial = sm.include_similar_

    await toggle_recommendations(message)

    assert sm.include_similar_ is not initial
    message.answer.assert_called_once()
