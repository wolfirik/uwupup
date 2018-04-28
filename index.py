import os
from discord.ext import commands
from discord.ext.commands import HelpFormatter
from data import Bot
from utils import permissions, default

config = default.get("config.json")
description = """
A simple starter bot code
Made by AlexFlipnote
"""


class HelpFormat(HelpFormatter):
    async def format_help_for(self, context, command_or_bot):
        if permissions.can_react(context):
            await context.message.add_reaction(chr(0x2709))

        return await super().format_help_for(context, command_or_bot)


print("Logging in...")
help_attrs = dict(hidden=True)
bot = Bot(command_prefix=commands.when_mentioned_or("owo "), prefix=commands.when_mentioned_or("owo "), pm_help=True, help_attrs=help_attrs, formatter=HelpFormat())

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        try:
            bot.load_extension(f"cogs.{name}")
        except:
            pass

bot.run(os.environ["TOKEN"])
