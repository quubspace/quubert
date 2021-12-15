import lightbulb
import hikari
import time

from hikari import Embed
from app.user import User

profiles = lightbulb.Plugin("Profiles")


@profiles.command()
@lightbulb.option(
    name="email", description="Your Quub-issued email", type=str, required=True
)
@lightbulb.option(
    name="name", description="Your full name: John Doe", type=str, required=True
)
@lightbulb.command(
    name="verify",
    description="Verifies your name and email, and adds you to the database.",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def verify(ctx: lightbulb.Context) -> None:
    try:
        await User.load(
            user_id=ctx.author.id, name=ctx.options.name, email=ctx.options.email
        )
        await ctx.respond("Successfully verified!")
    except Exception as e:
        await ctx.respond(f"There was an error in verifying you: {e}")


def load(bot) -> None:
    bot.add_plugin(profiles)


def unload(bot) -> None:
    bot.remove_plugin(profiles)
