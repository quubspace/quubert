import time
import hikari
import lightbulb
import re
import logging
import pandas as pd

from datetime import datetime, timedelta, date
from app.hours import Hours
from app import bot
from app.utils.helpers import (
    check_registration,
    preload_user_data,
    query_hours,
    hours_to_export,
)
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
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command(
    name="query_all",
    description="Check all users' hours. Usable only by owner.",
    ephemeral=True,
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def query_all(ctx: lightbulb.Context) -> None:
    if hours_list := await hours_to_export():
        message = f"Quub Timesheets for Week of {date.today() - timedelta(days=7)} to {date.today()}\n\n"

        try:
            # The bot object's users are not updating. This ensures the owner will always see the latest hours.
            # Plus, this command isn't used that often.
            user_data = await preload_user_data()
            users_hours = {
                user_id: tuple((user_data[user_id], [])) for (user_id, _) in hours_list
            }
        except Exception as e:
            logging.warning(f"Cannot gather hours: {e}")
            await ctx.respond("No registered users yet.")
            return

        for (user_id, hours) in hours_list:
            users_hours[user_id][1].append(hours)

        for (user, hours) in users_hours.values():
            total_hours_min = sum([x.quantity for x in hours])
            total_minutes = total_hours_min % 60
            total_hours_num = total_hours_min // 60

            total_quantity = f"{total_hours_num} hours and {total_minutes} minutes"

            message += (
                f"{user.name} has worked {total_quantity} this week. In detail:\n"
            )

            for entry in hours:
                hours_min = entry.quantity
                minutes = hours_min % 60
                hours_num = hours_min // 60

                quantity = f"{hours_num} hours and {minutes} minutes"

                message += f"- {entry.date}: {quantity}, {entry.description if entry.description else 'no description provided'}\n"

            message += "\n"

        await ctx.respond(message)
    else:
        await ctx.respond("No hours recorded this week.")


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

    if re.match(r"^-?\d+(:\d+)?$", ctx.options.quantity):
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
