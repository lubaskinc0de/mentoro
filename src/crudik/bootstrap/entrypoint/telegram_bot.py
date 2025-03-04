import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka
from redis.asyncio import Redis

from crudik.adapters.config import Config
from crudik.bootstrap.di.container import get_async_container
from crudik.presentation.bot.main import include_handlers


async def run_telegram_bot() -> None:
    logging.basicConfig(level=logging.INFO)
    config = Config.load_from_environment()
    bot = Bot(config.telegram_bot.token)
    redis = Redis.from_url(config.redis.connection_url)
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )
    dispatcher = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation(),
    )

    container = get_async_container(config)
    setup_dishka(container=container, router=dispatcher)
    setup_dialogs(dispatcher)
    include_handlers(dispatcher)

    logging.info("Telegram bot started")

    try:
        await dispatcher.start_polling(bot)
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(run_telegram_bot())
