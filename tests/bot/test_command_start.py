import pytest
from types import SimpleNamespace
from ConcertScheduleBot.__main__ import command_start_handler


@pytest.mark.asyncio
async def test_command_start_handler(mocker):
    message = mocker.AsyncMock()
    message.from_user = SimpleNamespace(id=1)
    message.chat = SimpleNamespace(id=1)

    await command_start_handler(message)

    message.answer.assert_called_once()
