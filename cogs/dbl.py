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
                channel = self.bot.get_channel(433715765129248770)
                await self.dblpy.post_server_count()
                up = await self.dblpy.get_upvotes()

                em = discord.Embed(title="DBL Update", description='<a:dblspin:393548363879940108> | Posted server count ({})\n'.format(len(self.bot.guilds)), color=0x7289da)
                await channel.send(embed=em)
                print(f"Servers: {len(self.bot.guilds)}\n Posted on dbl successfully.")
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

        


def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
