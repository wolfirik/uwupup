import random
import discord
import json
from collections import Counter
from discord.ext import commands
from utils import lists, permissions, http, default
import requests
import os


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
    @commands.is_nsfw()  # TODO: Remove this stupid reminder
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
        r = requests.get("https://sheri.fun/api/v1/bulges", headers={"key": os.environ["MURR"]})

        dick = discord.Embed(title="What's this~?", color=0xDEADBF)
        dick.set_image(url=r)

        try:
            await ctx.send(embed=dick)
            self.bot.counter["yiff_viewed"] += 1

        except discord.Forbidden:
            await ctx.send("aww i can't send embeds ;w;")
            
    @commands.command()
    @commands.is_nsfw()
    async def gay(self, ctx):
        """ 2 doods.🌈🌈🌈"""
        r = requests.get("https://sheri.fun/api/v1/gay", headers={"key": os.environ["MURR"]})

        dicks = discord.Embed(title="🌈", color=0xDEADBF)
        dicks.set_image(url=r)

        try:
            await ctx.send(embed=dicks)
            self.bot.counter["yiff_viewed"] += 1

        except discord.Forbidden:
            await ctx.send("aww i can't send embeds")
            
    @commands.command()
    @commands.is_nsfw()
    async def gif(self, ctx):
        """Animated yiff"""
        r = requests.get("https://sheri.fun/api/v1/bulges", headers={"key": os.environ["MURR"]})

        gyiff = discord.Embed(title="Have a gif", color=0xDEADBF)
        gyiff.set_image(url=r)

        try:
            await ctx.send(embed=gyiff)
            self.bot.counter["yiff_viewed"] += 1
            
        except discord.Forbidden:
            await ctx.send("aww i can't send embeds")
            
def setup(bot):
    bot.add_cog(NSFW(bot))
