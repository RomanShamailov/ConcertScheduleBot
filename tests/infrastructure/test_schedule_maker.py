import pytest
from ConcertScheduleBot.infrastructure.schedule_maker import ScheduleMaker


@pytest.mark.asyncio
async def test_schedule_bad_url(mock_session):
    maker = ScheduleMaker("bad_url", mock_session)

    result = await maker.schedule()

    assert result == "Кажется, это не ссылка на плейлист. Попробуй ещё раз."


@pytest.mark.asyncio
async def test_schedule_happy_path(mocker, mock_session):
    maker = ScheduleMaker(
        "https://music.yandex.ru/playlists/123",
        mock_session,
        include_similar=False,
    )

    mocker.patch.object(
        maker.parser_,
        "get_tracks_ids_list_from_playlist",
        return_value=[{"id": 1}],
    )

    mocker.patch.object(
        maker.parser_,
        "get_tracks_from_tracksids",
        return_value=[
            {
                "artists": [{"id": 10}],
            }
        ],
    )

    mocker.patch.object(
        maker.parser_,
        "get_concerts_from_artists",
        return_value=[
            {
                "concert": {
                    "id": 999,
                    "datetime": "2025-01-01T10:00:00",
                    "concertTitle": "Concert",
                    "city": "Berlin",
                },
                "minPrice": {"value": 50, "currency": "EUR"},
            }
        ],
    )

    result = await maker.schedule()

    assert "🎵 Концерты артистов из плейлиста" in result
    assert "🎤 Concert" in result
    assert "🌍 Berlin" in result
    assert "💵 Цена: 50 EUR" in result
