import asyncio
import logging
import os
import django
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from bot_code.database import db
from aiogram.fsm.storage.memory import MemoryStorage
from logging.handlers import RotatingFileHandler


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()





async def main():
    await db.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT"))
    )

    if await db.is_connected():
        print("✅ Database connected!")
    else:
        print("❌ Database connection failed!")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())


    from bot_code.handlers import base

    base.router.db = db
    dp.include_router(base.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                os.getenv("LOG_FILE", "bot.log"),
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ],
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

asyncio.run(main())


