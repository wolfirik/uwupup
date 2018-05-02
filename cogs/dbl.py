import dbl
import discord
from discord.ext import commands

import aiohttp
import asyncio
import logging
import os
from utils import repo

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ["DBL_TOKEN"]
        self.dblpy = dbl.Client(self.bot, self.token)
        

    @commands.command()
    @commands.cooldown(rate=1, per=1800, type=commands.BucketType.user)
    @commands.check(repo.is_owner)
    async def updated(self, ctx):
        """Updates server count on dbl"""
        try:
            await self.dblpy.post_server_count()
            await ctx.send(f"oki my dbl page now shows i'm in {len(self.bot.guilds)} guilds ^w^")
        except:
            await ctx.send("hmph.. there was an error.. try again later i guess..")

def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
