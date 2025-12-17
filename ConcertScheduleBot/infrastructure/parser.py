import aiohttp
import asyncio
from typing import Any
from .request_data import RequestData
from datetime import datetime


class Parser:

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session_ = session

    async def get_tracks_ids_list_from_playlist(self, api_url: str, cookies: dict[str, Any],
                                                headers: dict[str, Any]) -> list[dict[str, Any]] | str:
        params = {
            'resumeStream': 'false',
            'richTracks': 'false',
        }
        async with self.session_.get(
                url=api_url,
                params=params,
                cookies=cookies,
                headers=headers,
        ) as response:
            try:
                return (await response.json())['tracks']
            except KeyError:
                return f'error with text: {await response.text()}'

    async def get_tracks_from_tracksids(self, tracks_ids: list[dict[str, Any]], cookies: dict[str, Any],
                                        headers: dict[str, Any]) -> list[dict[str, Any]] | str:
        data = [('trackIds', f"{track['id']}") for track in tracks_ids]
        data.append(('removeDuplicates', 'false'))
        data.append(('withProgress', 'False'))
        async with self.session_.post(
                url='https://api.music.yandex.ru/tracks',
                cookies=cookies,
                headers=headers,
                data=data,
        ) as response:
            return await response.json()

    async def get_concerts_from_one_artist(self, artist_id: int, cookies: dict[str, Any],
                                           headers: dict[str, Any]) -> list[dict[str, Any]] | str:
        async with self.session_.get(
                url=f'https://api.music.yandex.ru/artists/{artist_id}/blocks/artist-concerts',
                cookies=cookies,
                headers=headers,
        ) as response:
            if response.status != 200:
                return f'banned with message {await response.text()}'
            try:
                return (await response.json())['concerts']
            except KeyError:
                return f'error with response {await response.text()}'

    async def get_concerts_from_artists(self, artists: set[int], cookies: dict[str, Any],
                                        headers: dict[str, Any]) -> list[dict[str, Any]]:
        tasks: list[asyncio.Task] = []
        for artist_id in artists:
            tasks.append(asyncio.create_task(self.get_concerts_from_one_artist(artist_id, cookies, headers)))
            await asyncio.sleep(RequestData.req_delay)
        concerts_packs: tuple[Any] = await asyncio.gather(*tasks)
        concerts: list[dict[str, Any]] = []
        for pack in concerts_packs:
            if type(pack) is not str:
                concerts.extend(pack)
        return sorted(
            concerts,
            key=lambda x: datetime.fromisoformat(x['concert']['datetime'])
        )

