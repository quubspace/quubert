import time
import hikari
import lightbulb
import re
import logging
import pandas as pd

from datetime import datetime
from app.hours import Hours
from app.utils.helpers import check_registration, query_hours
from hikari import Embed

timesheet = lightbulb.Plugin("Timesheet")


@timesheet.command()
@lightbulb.command(
    name="hours",
    description="Commands related to manipulating your timesheet.",
    ephemeral=True,
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hours(ctx: lightbulb.Context) -> None:
    if await check_registration(ctx.author.id):
        pass
    else:
        return


@hours.child
@lightbulb.command(
    name="query", description="Check the hours in timesheet.", ephemeral=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def query(ctx: lightbulb.Context) -> None:
    await query_hours(author_id=ctx.author.id, ctx=ctx)


@hours.child
@lightbulb.option(
    name="quantity", description="How many hours you worked.", type=str, required=True
)
@lightbulb.option(
    name="date",
    description="What day you worked on. In the format: YYYY-MM-DD",
    type=str,
    required=True,
)
@lightbulb.option(
    name="description",
    description="What you did. This is optional, but highly recommended.",
    type=str,
    required=False,
)
@lightbulb.command(
    name="add", description="Add hours to your timesheet.", ephemeral=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context) -> None:
    try:
        date = datetime.strptime(ctx.options.date, "%Y-%m-%d")
    except ValueError:
        await ctx.respond("Please enter a date in the valid format: YYYY-MM-DD!")
        return

    if re.match("^-?\d+(:\d+)?$", ctx.options.quantity):
        quantity = ctx.options.quantity.split(":")

        try:
            hours_num = abs(int(quantity[0]))
        except Exception as e:
            logging.warning(e)
            hours_num = 0

        try:
            min_num = abs(int(quantity[1]))
        except Exception as e:
            logging.warning(e)
            min_num = 0

        hours_min = (hours_num * 60) + min_num

        if ctx.options.quantity[0] == "-":
            hours_min *= -1
            hours_num = f"-{hours_num}"

    else:
        await ctx.respond("Please enter hours in the valid format - H:[m]!")
        return

    hours = await Hours.add(
        user_id=ctx.author.id,
        quantity=hours_min,
        datetime_obj=date,
        description=ctx.options.description,
    )

    await ctx.respond(
        f'Added {hours_num} hours and {min_num} minutes for {date.strftime("%Y-%m-%d")}: "{ctx.options.description}"'
    )

    await query_hours(author_id=ctx.author.id, ctx=ctx)


def load(bot) -> None:
    bot.add_plugin(timesheet)


def unload(bot) -> None:
    bot.remove_plugin(timesheet)
