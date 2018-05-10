import os
from discord.ext import commands
from discord.ext.commands import HelpFormatter
from data import Bot
from utils import permissions, default
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

config = default.get("config.json")
description = """
A simple starter bot code
Made by AlexFlipnote
"""


print("-w- zzz...")

bot = Bot(command_prefix=commands.when_mentioned_or("owo "), prefix=commands.when_mentioned_or("owo "), pm_help=True)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        try:
            bot.load_extension(f"cogs.{name}")
        except Exception as e:
            print(type(e).__name__)
            print(f"{e}")
            print(f"\nFailed to load {name}")
            pass

bot.run(os.environ["TOKEN"])
