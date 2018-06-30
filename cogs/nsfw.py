import random
import discord
import json
from collections import Counter
from discord.ext import commands
from utils import lists, permissions, http, default



class NSFW:
    def __init__(self, bot):
        self.bot = bot
        self.counter = Counter()
        self.config = default.get("config.json")

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        return r[endpoint]

    @commands.command()
    @commands.is_nsfw()  # TODO: Make a nsfw cog.
    async def yiff(self, ctx):
        """posts a yiff >:3c"""
        r = await self.randomimageapi(ctx, 'https://sheri.fun/api/v1/yiff', 'url')

        yiff = discord.Embed(title="heh", color=0xDEADBF)
        yiff.set_image(url=r)

        try:
            await ctx.send(embed=yiff)
            self.bot.counter["yiff_viewed"] += 1

        except discord.Forbidden:
            await ctx.send("aww i can't send embeds ;w;")

    @commands.command()
    @commands.is_nsfw()
    async def bulge(self, ctx):
        """you know what this is~"""
        r = random.choice(lists.bulges)

        yiff = discord.Embed(title="What's this~?", color=0xDEADBF)
        yiff.set_image(url=r)

        try:
            await ctx.send(embed=yiff)
            self.bot.counter["yiff_viewed"] += 1

        except discord.Forbidden:
            await ctx.send("aww i can't send embeds ;w;")

def setup(bot):
    bot.add_cog(NSFW(bot))