import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import user_handlers
from database.db import init_db

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(user_handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
