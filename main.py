import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.user import user
from dotenv import load_dotenv
import os


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_API_TOKEN'),
              default=DefaultBotProperties(parse_mode="MarkdownV2")
    )
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())