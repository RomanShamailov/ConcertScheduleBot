import pytest
from types import SimpleNamespace
from ConcertScheduleBot.__main__ import command_url_handler


@pytest.mark.asyncio
async def test_command_url_handler(mocker):
    message = mocker.AsyncMock()
    message.text = "https://music.yandex.ru/playlists/123"
    message.from_user = SimpleNamespace(id=1)
    message.chat = SimpleNamespace(id=1)

    progress_message = mocker.AsyncMock()
    message.answer.return_value = progress_message

    mocker.patch(
        "ConcertScheduleBot.__main__.start",
        return_value="РАСПИСАНИЕ",
    )

    await command_url_handler(message)

    progress_message.edit_text.assert_called_with("✅ Готово\n100%")

    message.answer.assert_any_call("РАСПИСАНИЕ")
