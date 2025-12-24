import aiohttp
from ConcertScheduleBot.infrastructure.schedule_maker import ScheduleMaker


async def start(playlist_url) -> str:
    return (await (ScheduleMaker(playlist_url=playlist_url, session=aiohttp.ClientSession()).schedule()))
