from bot.utils import config
from gino import Gino

db = Gino()

# import models so Gino registers them
import bot.database.models  # isort:skip


async def setup():
    await db.set_bind(config.database)


async def shutdown():
    await db.pop_bind().close()
