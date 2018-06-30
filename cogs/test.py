import sqlite3
import discord
from discord.ext import commands
from utils import default, repo, http
from io import BytesIO


class sql_test_cog:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    @commands.check(repo.is_owner)
    async def sql(self, ctx):
        """MEMES"""
        thing = BytesIO(await http.get(f"{ctx.author.avatar_url}".replace("webp", "png"), res_method="read"))
        myimage = Image.open(filename)
        myimage.load()


def setup(bot):
    bot.add_cog(sql_test_cog(bot))
