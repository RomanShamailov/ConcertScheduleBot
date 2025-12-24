from typing import Awaitable, Callable
import aiohttp
from ConcertScheduleBot.infrastructure.schedule_maker import ScheduleMaker


async def start(
    playlist_url,
    schedule_maker: ScheduleMaker | None = None,
    progress_callback: Callable[[int, str], Awaitable[None]] | None = None,
) -> str:
    if schedule_maker is None:
        schedule_maker = ScheduleMaker(playlist_url=playlist_url, session=aiohttp.ClientSession())
    else:
        schedule_maker.playlist_url_ = playlist_url
    return await schedule_maker.schedule(progress_callback=progress_callback)
