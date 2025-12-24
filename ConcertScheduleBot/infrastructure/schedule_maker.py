import aiohttp
import asyncio
from typing import Any, Awaitable, Callable
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
        include_similar: bool = True,
        similar_limit_per_artist: int = 1,
    ) -> None:
        self.playlist_url_ = playlist_url
        self.parser_ = Parser(session)
        self.include_similar_ = include_similar
        self.similar_limit_per_artist_ = similar_limit_per_artist

    async def _report_progress(
        self,
        callback: Callable[[int, str], Awaitable[None]] | None,
        percent: int,
        text: str,
    ) -> None:
        if callback:
            await callback(percent, text)

    async def schedule(
        self, progress_callback: Callable[[int, str], Awaitable[None]] | None = None
    ) -> str:
        await self._report_progress(progress_callback, 0, "Проверяю ссылку")
        api_url: str | None = PlaylistUrlToApiConvertor(self.playlist_url_).api_url()
        if api_url is None:
            await self._report_progress(
                progress_callback, 100, "Ошибка"
            )
            return "Кажется, это не ссылка на плейлист. Попробуй ещё раз."
        tracks_ids: (
            list[dict[str, Any]] | str
        ) = await self.parser_.get_tracks_ids_list_from_playlist(
            api_url,
            RequestData.req_data[0]["cookies"],
            RequestData.req_data[0]["headers"],
        )
        await self._report_progress(progress_callback, 20, "Получаю треки плейлиста")
        await asyncio.sleep(RequestData.req_delay)
        tracks = await self.parser_.get_tracks_from_tracksids(
            tracks_ids,
            RequestData.req_data[2]["cookies"],
            RequestData.req_data[2]["headers"],
        )
        await self._report_progress(progress_callback, 40, "Определяю артистов")
        await asyncio.sleep(RequestData.req_delay)
        artists_ids: set[int] = TracksToArtistsIdsConvertor(tracks).artists_ids()
        similar_artists_ids: set[int] | None = None
        if self.include_similar_:
            await self._report_progress(progress_callback, 55, "Собираю похожих артистов")
            similar_artists_ids = await self.parser_.get_similar_artists_from_artists(
                artists_ids,
                RequestData.req_data[1]["cookies"],
                RequestData.req_data[1]["headers"],
                limit_per_artist=self.similar_limit_per_artist_,
            )
            await asyncio.sleep(RequestData.req_delay)
        await self._report_progress(progress_callback, 70, "Собираю концерты")
        concerts: list[dict[str, Any]] = await self.parser_.get_concerts_from_artists(
            artists_ids,
            RequestData.req_data[3]["cookies"],
            RequestData.req_data[3]["headers"],
        )
        similar_concerts: list[dict[str, Any]] | None = None
        if self.include_similar_:
            similar_concerts: list[dict[str, Any]] = await self.parser_.get_concerts_from_artists(
                similar_artists_ids,
                RequestData.req_data[3]["cookies"],
                RequestData.req_data[3]["headers"],
            )
        await self._report_progress(progress_callback, 90, "Формирую расписание")
        return ConcertsToScheduleConvertor(concerts, similar_concerts).schedule()

    async def toggle_recs(self) -> None:
        self.include_similar_ = not self.include_similar_
