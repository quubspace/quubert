import lightbulb
import sys
import hikari
import bot.database as db

from bot.database.models import User
from pathlib import Path
from bot import utils, database
from dataclasses import dataclass

__version__ = "0.1.0"


@dataclass
class Bot:
    app: lightbulb.BotApp
    user_data: dict
    py_version: str
    version: str


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
    print(f"Logged in as {bot.app.get_me()}.")


def extensions():
    files = Path("bot", "extensions").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


def load_extensions(_bot):
    for ext in extensions():
        try:
            _bot.load_extensions(ext)
        except Exception as ex:
            print(f"Failed to load extension {ext} - exception: {ex}")


def run():
    load_extensions(bot.app)
    bot.app.run()
