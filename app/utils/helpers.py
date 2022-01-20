import lightbulb
import asyncio
import logging
import copy
import smtplib
import ssl
import app.database as db
import pandas as pd

from app.user import User
from datetime import date, timedelta
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


# TODO: Check if there are hours to export
async def hours_to_export() -> List:
    return list(
        set(
            tuple((hours.user_id, hours))
            for hours in bot.hours_data.values()
            if hours.date <= date.today()
            if hours.date >= (date.today() - timedelta(days=7))
        )
    )


async def send_timesheets():
    while True:
        # HACK: Change this to 300 for prod
        await asyncio.sleep(5)
        # TODO: Export to email
        if hours_list := await hours_to_export():
            logging.info("Emailing all current hours.")

            context = ssl.create_default_context()
            message = ""

            users_hours = {
                user_id: tuple((bot.user_data[user_id], []))
                for (user_id, _) in hours_list
            }

            for (user_id, hours) in hours_list:
                users_hours[user_id][1].append(hours)

            for (user, hours) in users_hours.values():
                message += f"{user.name} has worked {sum([x.quantity for x in hours])} hours this week. In detail:\n"
                for entry in hours:
                    message += f"- {entry.date}: {entry.quantity} hours, {entry.description if entry.description else 'no description provided'}\n"
                message += "\n"

            # HACK: Uncomment when ready to start sending
            # with smtplib.SMTP_SSL(
            #     config.smtp_host, config.email_port, context=context
            # ) as server:
            #     server.login(config.sender_email, config.email_password)
            #     server.sendmail(config.sender_email, config.receiver_email, message)

    # user_data = pd.read_sql_table("users", con=config.database)
    # hours_data = pd.read_sql_table("hours", con=config.database)

    # HACK: No need to wait during testing, but don't forget to uncomment for prod
    # if config.next_check == 0:
    #     td = timedelta(days=7)
    #     config.next_check = datetime.timestamp(datetime.utcnow() + td)
    #     config.store()
    # next_check = datetime.fromtimestamp(config.next_check)
    # wait = (next_check - datetime.utcnow()).total_seconds()
    # await asyncio.sleep(wait)
