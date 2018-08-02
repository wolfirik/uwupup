import sqlite3
import discord
from discord.ext import commands
from utils import default, repo, http
from io import BytesIO
from PIL import *

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
        
    @commands.command(pass_context=True, no_pm=True, aliases=['piltest'])
    async def pilt(self, ctx, *, message):
        if ctx.message.author.bot: return
        else:

            author = ctx.message.author
            channel = ctx.message.channel

            im = Image.open("config/red.jpg")

            draw = ImageDraw.Draw(im)

            w = im.size[0]
            h = im.size[1]

            font = ImageFont.truetype('arial.ttf', 100)
            f_w, f_h = font.getsize('PITEST')

            x = (w - f_w) / 2
            y = (h - f_h) / 2

            draw.text((x, y), message, font=font, fill=(0, 0, 0, 255))

            bytes = BytesIO()
            im.save(bytes, 'PNG')
            bytes.seek(0)

            await ctx.send(file=discord.File(bytes, filename='red.jpg'))
 


def setup(bot):
    bot.add_cog(sql_test_cog(bot))
