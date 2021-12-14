import lightbulb
import hikari
import time

from hikari import Embed
from bot import version, py_version

users = lightbulb.Plugin("Users")


@users.command()
@lightbulb.command(
    name="verify",
    description="Verifies your name and email, and adds you to the database.",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def verify(ctx: lightbulb.Context) -> None:
    await ctx.respond("invoked verify")


def load(bot):
    bot.add_plugin(users)


def unload(bot):
    bot.remove_plugin(users)
