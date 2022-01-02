import asyncio
import logging
import sys
import hikari
import lightbulb

from app import database, utils
from app.utils.helpers import preload_user_data, preload_hours_data, sync_data
from app.bot import Bot


__version__ = "0.1.0"
loop = asyncio.get_event_loop()

bot = Bot(
    app=lightbulb.BotApp(token=utils.config.token),
    user_data={},
    hours_data={},
    py_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    version=__version__,
)


@bot.app.listen()
async def on_ready(event: hikari.StartedEvent):
    await database.setup()
    bot.user_data = await preload_user_data()
    bot.hours_data = await preload_hours_data()

    asyncio.ensure_future(sync_data())

    logging.info(f"Logged in as {bot.app.get_me()}.")
