import lightbulb
import asyncio
import app.database as db

from app.user import User
from app.database.models import Hours as HoursModel, User as UserModel


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


async def sync_data():
    while True:
        try:
            user_data = await preload_user_data()
            if user_data:
                bot.user_data = user_data
            hours_data = await preload_hours_data()
            if hours_data:
                bot.hours_data = hours_data
        except:  # No idea why this is necessary, but breaks without it
            pass
        await asyncio.sleep(300)
