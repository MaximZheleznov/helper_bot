import asyncio
import config
from aiogram import Bot, Dispatcher
from handlers import key_handlers, command_handlers


async def main():
    bot = Bot(config.token)
    dp = Dispatcher()
    dp.include_router(key_handlers.router)
    dp.include_router(command_handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



