import lightbulb
import hikari
import time

from hikari import Embed
from app.user import User
from app.utils import config
from app.utils.helpers import check_registration
from app import bot

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
    if ctx.author.id in bot.user_data.keys():
        await ctx.respond("You are already verified!")
        return
    try:
        await User.load(
            user_id=ctx.author.id, name=ctx.options.name, email=ctx.options.email
        )
        await ctx.respond("Successfully verified!")
    except Exception as e:
        await ctx.respond(f"There was an error in verifying you: {e}")


@profiles.command()
@lightbulb.command(
    name="update", description="Commands related to updating your profile.."
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def update(ctx: lightbulb.Context) -> None:
    if await check_registration(ctx.author.id):
        pass
    else:
        return


@update.child
@lightbulb.option(
    name="new_email", description="Your Quub-issued email.", type=str, required=True
)
@lightbulb.command(name="email", description="Update the email on your profile.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def email(ctx: lightbulb.Context) -> None:
    user = await User.load(user_id=ctx.author.id)
    await user.update_email(ctx.options.new_email)
    await ctx.respond(f"Your new email: {bot.user_data[ctx.author.id].email}")


@update.child
@lightbulb.option(
    name="new_name", description="Your full name: John Doe", type=str, required=True
)
@lightbulb.command(name="name", description="Update the name on your profile.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def name(ctx: lightbulb.Context) -> None:
    user = await User.load(user_id=ctx.author.id)
    await user.update_name(ctx.options.new_name)
    await ctx.respond(f"Your new name: {bot.user_data[ctx.author.id].name}")


@profiles.command()
@lightbulb.command(
    name="profile",
    description="Displays basic information about a profile.",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    user = await User.load(user_id=ctx.author.id)
    embed = Embed(title=user.name, description=f"Email: `{user.email}`")
    embed.set_footer(text="Thank you for using Quubert!")
    await ctx.respond(embed=embed)


def load(app) -> None:
    app.add_plugin(profiles)


def unload(app) -> None:
    app.remove_plugin(profiles)
