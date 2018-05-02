import discord
from discord.ext import commands
import dbl
import aiohttp
import asyncio
import logging


class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ["DBL_TOKEN"] #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token, loop=bot.loop)
        self.updating = bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
       await self.bot.is_ready()
        while not bot.is_closed:
            print('Attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                print('Posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
