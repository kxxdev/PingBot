import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.database.models import async_main
from app.chat import chat

dp = Dispatcher()

async def main():
    bot = Bot(token=TOKEN)
    dp.include_routers(chat)
    print('START')
    await dp.start_polling(bot)

async def on_startup():
    await async_main()

if __name__ == '__main__':
    asyncio.run(on_startup())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass