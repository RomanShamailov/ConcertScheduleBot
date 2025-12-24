import aiohttp
import asyncio
from typing import Any
from ConcertScheduleBot.infrastructure.parser import Parser
from ConcertScheduleBot.infrastructure.request_data import RequestData
from ConcertScheduleBot.adapters.conversions_for_parsing import (
    PlaylistUrlToApiConvertor,
    TracksToArtistsIdsConvertor,
    ConcertsToScheduleConvertor,
)


class ScheduleMaker:
    def __init__(
        self,
        playlist_url: str,
        session: aiohttp.ClientSession,
        include_similar: bool = False,
        similar_limit_per_artist: int = 5,
    ) -> None:
        self.playlist_url_ = playlist_url
        self.parser_ = Parser(session)
        self.include_similar_ = include_similar
        self.similar_limit_per_artist_ = similar_limit_per_artist

    async def schedule(self) -> str:
        api_url: str | None = PlaylistUrlToApiConvertor(self.playlist_url_).api_url()
        if api_url is None:
            return "Кажется, это не ссылка на плейлист. Попробуй ещё раз."
        tracks_ids: (
            list[dict[str, Any]] | str
        ) = await self.parser_.get_tracks_ids_list_from_playlist(
            api_url,
            RequestData.req_data[0]["cookies"],
            RequestData.req_data[0]["headers"],
        )
        if isinstance(tracks_ids, str):
            return tracks_ids
        await asyncio.sleep(RequestData.req_delay)
        tracks = await self.parser_.get_tracks_from_tracksids(
            tracks_ids,
            RequestData.req_data[2]["cookies"],
            RequestData.req_data[2]["headers"],
        )
        if isinstance(tracks, str):
            return tracks
        await asyncio.sleep(RequestData.req_delay)
        artists_ids: set[int] = TracksToArtistsIdsConvertor(tracks).artists_ids()

        all_artists_ids = artists_ids.copy() #TODO: надо ли копировать?
        if self.include_similar_:
            similar_artists_ids = await self.parser_.get_similar_artists_from_artists(
                artists_ids,
                RequestData.req_data[1]["cookies"],
                RequestData.req_data[1]["headers"],
                limit_per_artist=self.similar_limit_per_artist_,
            )
            all_artists_ids.update(similar_artists_ids)
            await asyncio.sleep(RequestData.req_delay)

        concerts: list[dict[str, Any]] = await self.parser_.get_concerts_from_artists(
            all_artists_ids,
            RequestData.req_data[3]["cookies"],
            RequestData.req_data[3]["headers"],
        )
        return ConcertsToScheduleConvertor(concerts).schedule()
