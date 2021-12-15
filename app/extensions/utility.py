import lightbulb
import hikari
import time

from hikari import Embed
from app import bot

utility = lightbulb.Plugin("Utility")


@utility.command()
@lightbulb.command(name="ping", description="Checks that the bot is alive")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    """Checks that the bot is alive"""
    embed = Embed(title="Ping", description="Speed and latency of bot.")
    before_time = time.time()
    msg = await ctx.respond(embed=embed)
    elapsed_ms = round((time.time() - before_time) * 1000)
    embed.add_field(name="Ping", value=f"{elapsed_ms}ms")
    await msg.edit(embed=embed)


@utility.command()
@lightbulb.command(name="info", description="Displays basic information about the bot.")
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    """Shows stats and infos about the bot"""
    embed = Embed(title="Quubert", description="Information about Quubert bot.")
    embed.add_field(
        name="Software Versions",
        value=f"```py\n"
        f"Quubert: {bot.version}\n"
        f"Hikari: {hikari.__version__}\n"
        f"Lightbulb: {lightbulb.__version__}\n"
        f"Python: {bot.py_version}```",
        inline=False,
    )
    embed.set_footer(text="Thank you for using Quubert!")
    await ctx.respond(embed=embed)


@utility.command()
@lightbulb.option(name="text", description="Text to repeat", type=str)
@lightbulb.command(name="echo", description="Repeats the user's input")
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)


def load(bot):
    bot.add_plugin(utility)


def unload(bot):
    bot.remove_plugin(utility)
