import lightbulb
import asyncio
import logging
import copy
import smtplib
import ssl
import app.database as db
import pandas as pd

from app.user import User
from app.hours import Hours
from datetime import date, timedelta, datetime
from typing import List
from app.utils import config
from app.database.models import Hours as HoursModel, User as UserModel
from app.bot import Bot
from app import bot


async def check_registration(ctx: lightbulb.Context, user_id: int):
    user = await User.load(user_id=user_id)
    if user is None:
        await ctx.respond(
            "You are not registered! Please verify before updating your profile."
        )
        return False
    else:
        return True


async def preload_user_data():
    users = await UserModel.query.gino.all()
    return {user.id: user for user in users}


async def preload_hours_data():
    all_hours = await HoursModel.query.gino.all()
    return {hours.id: hours for hours in all_hours}


async def preload_data():
    try:
        user_data = await preload_user_data()
        bot.user_data = user_data

        hours_data = await preload_hours_data()
        bot.hours_data = hours_data
    except:  # No idea why this is necessary, but breaks without it
        pass


async def query_hours(author_id: int, ctx: lightbulb.Context):
    hours = await Hours.load(user_id=author_id)
    if hours:
        hours_min = sum([x.quantity for x in hours])
        minutes = hours_min % 60
        hours = hours_min // 60

        quantity = f"{hours} hours and {minutes} minutes"
    else:
        quantity = "no hours"

    await ctx.respond(f"You have worked {quantity} this week.")


async def hours_to_export() -> List:
    try:
        bot_hours = bot.hours_data.values()
    except AttributeError:
        bot_hours = []

    return list(
        set(
            tuple((hours.user_id, hours))
            for hours in bot_hours
            if hours.date <= date.today()
            if hours.date >= (date.today() - timedelta(days=7))
        )
    )


async def send_timesheets():
    while True:
        await asyncio.sleep(5)

        if hours_list := await hours_to_export():
            if (
                config.smtp_host is None
                or config.email_port is None
                or config.sender_email is None
                or config.receiver_email is None
                or config.email_password is None
            ):
                logging.warning("Config not complete. Not sending any timesheets.")
                return

            logging.info("Emailing all current hours.")

            context = ssl.create_default_context()
            message = f"SUBJECT: Quub Timesheets for Week of {date.today() - timedelta(days=7)} to {date.today()}\n\n"

            users_hours = {
                user_id: tuple((bot.user_data[user_id], []))
                for (user_id, _) in hours_list
            }

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

            with smtplib.SMTP_SSL(
                config.smtp_host, config.email_port, context=context
            ) as server:
                server.login(config.sender_email, config.email_password)
                server.sendmail(config.sender_email, config.receiver_email, message)
        else:
            logging.info("No hours to send.")

        if int(config.next_check) == 0:
            td = timedelta(days=7)
            config.next_check = datetime.timestamp(datetime.utcnow() + td)
            config.store()
        next_check = datetime.fromtimestamp(int(config.next_check))
        wait = (next_check - datetime.utcnow()).total_seconds()
        await asyncio.sleep(wait)
