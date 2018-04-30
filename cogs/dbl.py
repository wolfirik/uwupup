import dbl
import discord
from discord.ext import commands

import aiohttp
import asyncio
import logging
import os

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ["DBL_TOKEN"]
        self.dblpy = dbl.Client(self.bot, self.token, bot=bot.loop)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            try:
                await self.dblpy.post_server_count()
                print(f"Servers: {len(self.bot.guilds)}\n Posted on dbl successfully.")
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

        


def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
