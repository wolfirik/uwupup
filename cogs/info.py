import time
import discord
import psutil
import os

from discord.ext import commands
from datetime import datetime
from utils import repo, default


class Information:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    def get_bot_uptime(self, *, brief=False):
        now = datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong `Edit:` {int(ping)}ms | `Bot speed:` {self.bot.latency}ms")

    @commands.command(aliases=['joinme', 'join', 'botinvite'])
    async def links(self, ctx):
        """ Invite me to your server """
        invite = discord.Embed(description="[invite me OwO](https://discordapp.com/oauth2/authorize?client_id=365255872181567489&scope=bot&permissions=470150214)\n[join the support guild if you have questions uwu](https://discord.gg/tBrtd)", color=0x254d16)
        await ctx.send(embed=invite)

    @commands.command(aliases=['upvote'])
    async def vote(self, ctx):
        """Gimme an upvote if you like me uwu"""
        await ctx.send(f"{ctx.author.mention} Upvoting me here would be greatly appriciated ^w^\nhttps://discordbots.org/bot/365255872181567489/vote")

   # @commands.command()
   # @commands.cooldown(rate=2, per=900, type=commands.BucketType.user)
   # async def suggest(self, ctx, *, suggestion_txt: str):
    #    """ Send a suggestion to my owner or just tell him hes doing a bad job -w- """
    #    channel = self.bot.get_channel(409168557147160587)
     #   suggestion = suggestion_txt
      #  if len(suggestion) >= 2000:
      #      ctx.send(f"xwx {ctx.author.mention} thats a bit too long for me to send. Shorten it and try again. (2000 character limit)")
       # else:
        #    try:
         #       ctx.send("oki! your suggestion has been sent successfully! ^w^")
          #      suggestionem = discord.Embed(title=f"From {ctx.author}", description=f"{suggestion}") 
           #     channel.send(embed=suggestionem)
            #except Exception as e:
             #   print(e)
# not working x~x

    @commands.command()
    async def source(self, ctx):
        """ Credits """
        await ctx.send(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/xelA/discord_bot.py")

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        color = 0x33353
        owner = self.bot.get_user(158750488563679232)

        embed = discord.Embed(colour=color)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Uptime", value=self.get_bot_uptime(), inline=False)
        embed.add_field(name="Dev", value=f"{owner}", inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=len(ctx.bot.guilds), inline=True)
        embed.add_field(name="Commands used", value=self.bot.counter["cmds_ran"], inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
