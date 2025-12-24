import asyncio
import os
import aiohttp
from ConcertScheduleBot.infrastructure.schedule_maker import ScheduleMaker
from ConcertScheduleBot.infrastructure.start_for_test import start

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

token_value = os.getenv("BOT_TOKEN")
if token_value is None:
    raise RuntimeError("BOT_TOKEN is not set")
TOKEN: str = token_value

dp = Dispatcher()
TOGGLE_OFF_TEXT = "Выключить рекомендации"
TOGGLE_ON_TEXT = "Включить рекомендации"
user_schedule_makers: dict[int, ScheduleMaker] = {}


def user_keyboard(include_similar: bool) -> ReplyKeyboardMarkup:
    button_text = TOGGLE_OFF_TEXT if include_similar else TOGGLE_ON_TEXT
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text)]], resize_keyboard=True
    )


def get_user_id(message: Message) -> int:
    return message.from_user.id if message.from_user else message.chat.id


def get_schedule_maker(user_id: int) -> ScheduleMaker:
    schedule_maker = user_schedule_makers.get(user_id)
    if schedule_maker is None:
        session = aiohttp.ClientSession()
        schedule_maker = ScheduleMaker(playlist_url="", session=session)
        user_schedule_makers[user_id] = schedule_maker
    return schedule_maker


@dp.message(F.text.in_([TOGGLE_OFF_TEXT, TOGGLE_ON_TEXT]))
async def toggle_recommendations(message: Message) -> None:
    schedule_maker = get_schedule_maker(get_user_id(message))
    await schedule_maker.toggle_recs()
    status_text = (
        "Рекомендации включены."
        if schedule_maker.include_similar_
        else "Рекомендации отключены."
    )
    await message.answer(
        status_text,
        reply_markup=user_keyboard(schedule_maker.include_similar_)
    )


MAX_LEN = 4096


def split_message(text: str, max_len: int = MAX_LEN):
    lines = text.splitlines(keepends=True)
    chunk = ""
    for line in lines:
        if len(chunk) + len(line) > max_len:
            if chunk:
                yield chunk
                chunk = ""
            while len(line) > max_len:
                yield line[:max_len]
                line = line[max_len:]
        chunk += line
    if chunk:
        yield chunk


@dp.message(~CommandStart(), ~F.text.in_([TOGGLE_OFF_TEXT, TOGGLE_ON_TEXT]))
async def command_url_handler(message: Message) -> None:
    schedule_maker = get_schedule_maker(get_user_id(message))
    progress_message = await message.answer("⏳ Готовлю расписание...\n0%")

    async def progress(percent: int, text: str) -> None:
        await progress_message.edit_text(f"⏳ {text}\n{percent}%")

    schedule: str = await start(
        message.text, schedule_maker=schedule_maker, progress_callback=progress
    )
    await progress_message.edit_text("✅ Готово\n100%")
    for part in split_message(schedule, MAX_LEN):
        await message.answer(part)
    await message.answer(
        "Я вновь готов составить расписание, только отправь мне ссылку.",
        reply_markup=user_keyboard(schedule_maker.include_similar_),
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    schedule_maker = get_schedule_maker(get_user_id(message))
    await message.answer(
        "Привет! Отправь мне ссылку на плейлист и я \
            составлю расписание концертов твоих артистов.",
        reply_markup=user_keyboard(schedule_maker.include_similar_),
    )


@dp.shutdown()
async def on_shutdown() -> None:
    sessions = {
        id(schedule_maker.parser_.session_): schedule_maker.parser_.session_
        for schedule_maker in user_schedule_makers.values()
    }
    for session in sessions.values():
        if not session.closed:
            await session.close()


async def main() -> None:
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
