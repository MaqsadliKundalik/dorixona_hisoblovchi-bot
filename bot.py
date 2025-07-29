from aiogram import Bot, Dispatcher
from asyncio import run
from config import TOKEN
from database import init as init_db
from handlers import router
from logging import basicConfig, INFO

dp = Dispatcher()
dp.include_router(router)

async def main():
    basicConfig(level=INFO)
    bot = Bot(token=TOKEN)
    await init_db()
    await dp.start_polling(bot)

run(main=main())