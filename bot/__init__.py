import lightbulb
import sys
import hikari

from pathlib import Path
from bot.utils import config

bot = lightbulb.BotApp(token=config.token)

version = "0.1.0"
py_version = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)


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
    load_extensions(bot)
    bot.run()
