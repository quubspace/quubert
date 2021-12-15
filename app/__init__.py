import lightbulb
import logging
import sys
import hikari
import app.database as db
import asyncio

from app.database.models import User
from app import utils, database
from app.bot import Bot
from dataclasses import dataclass

__version__ = "0.1.0"
loop = asyncio.get_event_loop()

bot = Bot(
    app=lightbulb.BotApp(token=utils.config.token),
    user_data={},
    py_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    version=__version__,
)


async def preload_user_data():
    users = await User.query.gino.all()
    return {f"{user.id}": user for user in users}


async def sync_user_data():
    while True:
        try:
            user_data = await preload_user_data()
            if user_data:
                bot.user_data = user_data
        except:  # No idea why this is necessary, but breaks without it
            pass
        await asyncio.sleep(300)


@bot.app.listen()
async def on_ready(event: hikari.StartedEvent):
    await database.setup()
    bot.user_data = await preload_user_data()

    asyncio.ensure_future(sync_user_data())

    logging.info(f"Logged in as {bot.app.get_me()}.")
