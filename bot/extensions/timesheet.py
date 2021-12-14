import lightbulb
import hikari
import time

from hikari import Embed
from bot import version, py_version

timesheet = lightbulb.Plugin("Timesheet")


@timesheet.command()
@lightbulb.command(name="hours", description="Checks that the bot is alive")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hours(ctx: lightbulb.Context) -> None:
    pass


@hours.child
@lightbulb.command(name="add", description="test subcommand")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context) -> None:
    await ctx.respond("invoked hours add")


def load(bot):
    bot.add_plugin(timesheet)


def unload(bot):
    bot.remove_plugin(timesheet)
