import os
from discord.ext import commands
from discord.ext.commands import HelpFormatter
from data import Bot
from utils import permissions, default
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

config = default.get("config.json")
description = """
A simple starter bot code
Made by AlexFlipnote
"""


print("-w- zzz...")

bot = Bot(command_prefix=commands.when_mentioned_or("owo "), prefix=commands.when_mentioned_or("owo "), pm_help=True)

def init_function(bot):
	global cursor, engine, Session
	if bot.dev_mode:
		db = 'owo'
	elif bot.self_bot:
		db = 'owo'
	else:
		db = 'owo'
	engine = create_engine('mysql+pymysql://0:@localhost/{1}?charset=utf8mb4'.format(db), encoding='utf8')
	session_factory = sessionmaker(bind=engine)
	Session = scoped_session(session_factory)
	bot.mysql = Object()
	engine = bot.mysql.engine = engine
	cursor = bot.mysql.cursor = bot.get_cursor


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
