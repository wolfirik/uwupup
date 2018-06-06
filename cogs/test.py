import sqlite3
import discord
from discord.ext import commands
from utils import default, repo, http
from io import BytesIO
import PIL

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
         await ctx.send("done")
         conn.close()

     @commands.command()
     @commands.check(repo.owner)
     async def color(self, ctx):
         bio = BytesIO(await http.get(ctx.author.avatar_url.replace("webp", "png"), res_method="read"))
         img = await PIL.ImageOps.colorize(bio, rgb(255,0,0), rgb(153,0,0))
         final = BytesIO()
         img = img.save(final, 'png')
         await ctx.send(file=discord.File(img, filename="color.png"))

def setup(bot):
    bot.add_cog(sql_test_cog(bot))
