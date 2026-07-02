import asyncio
import config
from aiogram import Bot, Dispatcher
from routers.tg_save_link import router as bot_router
from routers.tg_save_link import maintenance_router as m_router


async def main():
    bot = Bot(config.token)
    dp = Dispatcher()
    dp.include_router(bot_router)
    dp.include_router(m_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
