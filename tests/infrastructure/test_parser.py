import pytest
from ConcertScheduleBot.infrastructure.parser import Parser
from unittest.mock import AsyncMock


# get_tracks_ids_list_from_playlist
@pytest.mark.asyncio
async def test_get_tracks_ids_list_success(mock_session):
    response = AsyncMock()
    response.json.return_value = {"tracks": [{"id": 1}]}
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    result = await parser.get_tracks_ids_list_from_playlist("url", {}, {})

    assert result == [{"id": 1}]


@pytest.mark.asyncio
async def test_get_tracks_ids_list_key_error(mock_session):
    response = AsyncMock()
    response.json.return_value = {}
    response.text.return_value = "error"
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    result = await parser.get_tracks_ids_list_from_playlist("url", {}, {})

    assert result.startswith("error with text")


# get_concerts_from_one_artist
@pytest.mark.asyncio
async def test_get_concerts_from_one_artist_success(mock_session):
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {
        "concerts": [{"concert": {"datetime": "2025-01-01T10:00:00"}}]
    }
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    concerts = await parser.get_concerts_from_one_artist(1, {}, {})

    assert isinstance(concerts, list)


@pytest.mark.asyncio
async def test_get_concerts_from_one_artist_banned(mock_session):
    response = AsyncMock()
    response.status = 403
    response.text.return_value = "banned"
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    result = await parser.get_concerts_from_one_artist(1, {}, {})

    assert result.startswith("banned with message")

@pytest.mark.asyncio
async def test_get_similar_artists_success(mock_session):
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {
        "similarArtists": [
            {"id": 100, "name": "Artist 1"},
            {"id": 200, "name": "Artist 2"},
            {"id": 300, "name": "Artist 3"},
        ]
    }
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    result = await parser.get_similar_artists_from_one_artist(1, {}, {})

    assert result == [100, 200, 300]

@pytest.mark.asyncio
async def test_get_similar_artists_not_found(mock_session):
    response = AsyncMock()
    response.status = 404
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    result = await parser.get_similar_artists_from_one_artist(1, {}, {})

    assert result == []

@pytest.mark.asyncio
async def test_get_similar_artists_empty(mock_session):
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {}
    mock_session.get.return_value.__aenter__.return_value = response

    parser = Parser(mock_session)
    result = await parser.get_similar_artists_from_one_artist(1, {}, {})

    assert result == []

