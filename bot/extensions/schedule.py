import lightbulb
import hikari
import time

from hikari import Embed
from bot import version, py_version

scheduling = lightbulb.Plugin("Scheduling")


@scheduling.command()
@lightbulb.command(
    name="schedule",
    description="Displays the schedule for the next two weeks.",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def schedule(ctx: lightbulb.Context) -> None:
    await ctx.respond("invoked schedule")


@scheduling.command()
@lightbulb.command(
    name="event",
    description="Commands relating to the schedule",
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def event(ctx: lightbulb.Context) -> None:
    pass


@event.child
@lightbulb.command(
    name="add",
    description="Adds event to the schedule",
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context) -> None:
    await ctx.respond("invoked event add")


def load(bot):
    bot.add_plugin(scheduling)


def unload(bot):
    bot.remove_plugin(scheduling)
