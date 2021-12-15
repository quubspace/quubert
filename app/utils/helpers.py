import lightbulb

from app.user import User


async def check_registration(ctx: lightbulb.Context, user_id: int):
    user = await User.load(user_id=user_id)
    if user is None:
        await ctx.respond(
            "You are not registered! Please verify before updating your profile."
        )
        return False
    else:
        return True
