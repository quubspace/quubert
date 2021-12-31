import asyncio
import logging
import sys
from dataclasses import dataclass

import hikari
import lightbulb

import app.database as db
from app import database, utils
from app.bot import Bot
from app.database.models import Hours, User

__version__ = "0.1.0"
loop = asyncio.get_event_loop()

bot = Bot(
    app=lightbulb.BotApp(token=utils.config.token),
    user_data={},
    hours_data={},
    py_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    version=__version__,
)


async def preload_user_data():
    users = await User.query.gino.all()
    return {user.id: user for user in users}


async def preload_hours_data():
    all_hours = await Hours.query.gino.all()
    return {hours.id: hours for hours in all_hours}


async def sync_data():
    while True:
        try:
            user_data = await preload_user_data()
            if user_data:
                bot.user_data = user_data
            hours_data = await preload_hours_data()
            if hours_data:
                bot.hours_data = hours_data
        except:  # No idea why this is necessary, but breaks without it
            pass
        await asyncio.sleep(300)


@bot.app.listen()
async def on_ready(event: hikari.StartedEvent):
    await database.setup()
    bot.user_data = await preload_user_data()

    asyncio.ensure_future(sync_data())

    logging.info(f"Logged in as {bot.app.get_me()}.")
