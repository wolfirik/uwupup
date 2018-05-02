import discord
from discord.ext import commands
from utils.dataIO import dataIO
import os
import asyncio
from random import choice as rand

# interpreting from irdumbs welcome cog

de_greeting = "hai {0.mention}! Welcome to {1.name}!"
de_settings = {"MSGS": [de_greeting], "ON": False, "CHANNEL": None}
path = "data/welcome/settings.json"

class Welcome:
    """Cog for welcoming new users to the server"""
       

    def __init__(self, bot):
      self.bot = bot
      self.settings = dataIO.load_json(path)
