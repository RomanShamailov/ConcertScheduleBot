import asyncio
from ConcertScheduleBot.infrastructure.start_for_test import start

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

dp = Dispatcher()


@dp.message(~CommandStart())
async def command_url_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    schedule: str = await start(message.text)
    await message.reply(schedule)
    await message.answer("Я вновь готов составить расписание, только отправь мне ссылку.")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Привет! Отправь мне ссылку на плейлист и я составлю расписание концертов твоих артистов.")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
