import lightbulb
import logging
import sys
import hikari
import app.database as db

from app.database.models import User
from app import utils, database
from app.bot import Bot
from dataclasses import dataclass

__version__ = "0.1.0"

bot = Bot(
    app=lightbulb.BotApp(token=utils.config.token),
    user_data={},
    py_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    version=__version__,
)


async def preload_user_data():
    users = await User.query.gino.all()
    return {f"{user.id}": user for user in users}


@bot.app.listen()
async def on_ready(event: hikari.StartedEvent):
    await database.setup()
    bot.user_data = await preload_user_data()
    logging.info(f"Logged in as {bot.app.get_me()}.")
