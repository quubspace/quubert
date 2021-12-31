import time

import hikari
import lightbulb
import pandas as pd
from app.hours import Hours
from app.utils.helpers import check_registration
from hikari import Embed

timesheet = lightbulb.Plugin("Timesheet")


@timesheet.command()
@lightbulb.command(
    name="hours",
    description="Commands related to manipulating your timesheet.",
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hours(ctx: lightbulb.Context) -> None:
    if await check_registration(ctx.author.id):
        pass
    else:
        return


@hours.child
@lightbulb.command(name="query", description="Check the hours in timesheet.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def query(ctx: lightbulb.Context) -> None:
    hours = await Hours.load(user_id=ctx.author.id)
    await ctx.respond(f"You have worked {hours.quantity} hours.")


@hours.child
@lightbulb.command(name="add", description="Add hours to your timesheet.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context) -> None:
    await ctx.respond("invoked hours add")


def load(bot) -> None:
    bot.add_plugin(timesheet)


def unload(bot) -> None:
    bot.remove_plugin(timesheet)
