# this cog is being used to manage data if i get it working i can do commands like welcoming or mod logs
import rethinkdb as r
import discord
from discord.ext import commands
from utils import repo

class db_test:
    def __init__(self, bot):
        self.bot = bot
        self.conn = r.connect(db='owo')

    @commands.command(name='dbtest')
    @commands.check(repo.is_owner)
    async def rethink(self, ctx):
        """Tests the rethink api used for future data management"""
        try:
            data = r.db_create('owodata').run(self.conn)
            await ctx.send(data)
        except:
            await ctx.send("oof")
    
  def setup(bot):
    bot.add_cog(db_test(bot))
