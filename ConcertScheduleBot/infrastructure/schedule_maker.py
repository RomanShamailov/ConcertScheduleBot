import aiohttp
import asyncio
from typing import Any
from .parser import Parser
from .request_data import RequestData
from ..adapters.conversions_for_parsing import PlaylistUrlToApiConvertor, TracksToArtistsIdsConvertor, ConcertsToScheduleConvertor


class ScheduleMaker:

    def __init__(self, playlist_url: str, session: aiohttp.ClientSession) -> None:
        self.playlist_url_ = playlist_url
        self.parser_ = Parser(session)

    async def schedule(self) -> str:
        api_url: str | None = PlaylistUrlToApiConvertor(self.playlist_url_).api_url()
        if api_url is None:
            return f'bad url'
        tracks_ids: list[dict[str, Any]] | str =\
            await self.parser_.get_tracks_ids_list_from_playlist(api_url, RequestData.req_data[0]['cookies'],
                                                                 RequestData.req_data[0]['headers'])
        if type(tracks_ids) is str:
            return tracks_ids
        await asyncio.sleep(RequestData.req_delay)
        tracks = await self.parser_.get_tracks_from_tracksids(tracks_ids, RequestData.req_data[2]['cookies'],
                                                              RequestData.req_data[2]['headers'])
        if type(tracks) is str:
            return tracks
        await asyncio.sleep(RequestData.req_delay)
        artists_ids: set[int] = TracksToArtistsIdsConvertor(tracks).artists_ids()
        concerts: list[dict[str, Any]] =\
            await self.parser_.get_concerts_from_artists(artists_ids, RequestData.req_data[3]['cookies'],
                                                         RequestData.req_data[3]['headers'])
        return ConcertsToScheduleConvertor(concerts).schedule()
