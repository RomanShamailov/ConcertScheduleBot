import pytest
from ConcertScheduleBot.adapters.conversions_for_parsing import (
    PlaylistUrlToApiConvertor,
    TracksToArtistsIdsConvertor,
    ConcertsToScheduleConvertor,
)


# PlaylistUrlToApiConvertor
@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://music.yandex.ru/playlists/abc",
            "https://api.music.yandex.ru/playlist/abc",
        ),
        (
            "https://music.yandex.ru/users/user1/playlists/1",
            "https://api.music.yandex.ru/users/user1/playlists/1",
        ),
    ],
)
def test_playlist_url_to_api_convertor_valid(url, expected):
    converter = PlaylistUrlToApiConvertor(url)
    assert converter.api_url() == expected


def test_playlist_url_to_api_convertor_invalid():
    converter = PlaylistUrlToApiConvertor("https://google.com")
    assert converter.api_url() is None


# TracksToArtistsIdsConvertor
def test_tracks_to_artists_ids_unique():
    tracks = [
        {"artists": [{"id": 1}, {"id": 2}]},
        {"artists": [{"id": 2}, {"id": 3}]},
    ]

    converter = TracksToArtistsIdsConvertor(tracks)
    assert converter.artists_ids() == {1, 2, 3}


# ConcertsToScheduleConvertor
def test_concerts_to_schedule_happy_path():
    concerts = [
        {
            "concert": {
                "datetime": "2025-01-01T20:00:00",
                "concertTitle": "Live Show",
                "city": "Moscow",
            },
            "minPrice": {"value": 1000, "currency": "RUB"},
        }
    ]

    schedule = ConcertsToScheduleConvertor(concerts).schedule()

    assert "2025-01-01T20:00:00: Live Show" in schedule
    assert "price: 1000RUB" in schedule
    assert "city: Moscow" in schedule


def test_concerts_to_schedule_with_invalid_concert():
    concerts = [{}]

    schedule = ConcertsToScheduleConvertor(concerts).schedule()

    assert schedule.strip() == ""
