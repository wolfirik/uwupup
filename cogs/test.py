import sqlite3
import discord
from discord.ext import commands
from utils import default

class sql_test_cog:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    @commands.check(repo.is_owner)
    async def sql(self, ctx):
        """MEMES"""
        conn = sqlite3.connect('owo.db')
        conn.execute('''CREATE TABLE BADGES
          (BADGE_NAME      TEXT    NOT NULL,
          EMOTE           TEXT    NOT NULL,
          DESCRIPTION     TEXT    NOT NULL);''')
       conn.close()
       await ctx.send("done")

def setup(bot):
    bot.add_cog(sql_test_cog(bot))
