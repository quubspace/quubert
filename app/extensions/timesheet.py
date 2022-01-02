import time
import hikari
import lightbulb
import pandas as pd

from datetime import datetime
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
    quantity = sum([x.quantity for x in hours]) if hours else "no"

    await ctx.respond(f"You have worked {quantity} hours this week.")


@hours.child
@lightbulb.option(
    name="quantity", description="How many hours you worked.", type=int, required=True
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
@lightbulb.command(name="add", description="Add hours to your timesheet.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context) -> None:
    try:
        date = datetime.strptime(ctx.options.date, "%Y-%m-%d")
    except ValueError:
        await ctx.respond("Please enter a date in the valid format: YYYY-MM-DD!")
        return

    hours = await Hours.add(
        user_id=ctx.author.id,
        quantity=ctx.options.quantity,
        date=date,
        description=ctx.options.description,
    )

    await ctx.respond(
        f'Added {ctx.options.quantity} hours for {date.strftime("%Y-%m-%d")}: "{ctx.options.description}"'
    )


def load(bot) -> None:
    bot.add_plugin(timesheet)


def unload(bot) -> None:
    bot.remove_plugin(timesheet)
