import time
import discord
import psutil
import os

from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
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
        await message.edit(content=f"Pong!\n`Edit {int(ping)}ms\nAPI {self.bot.latency}ms`")

    @commands.command(aliases=['joinme', 'links', 'botinvite'])
    async def invite(self, ctx):
        """ Invite me to your server """
        server = self.bot.get_emoji(314003252830011395)
        bottag = self.bot.get_emoji(230105988211015680)
        invite = discord.Embed(title="Bot link", description=f"{bottag}[**Bot Invite**](https://discordapp.com/oauth2/authorize?client_id=365255872181567489&scope=bot&permissions=470150214)\n{server}[**Support Guild Invite**](https://discord.gg/tBrtd)", color=0x254d16)
        await ctx.send(embed=invite)

    @commands.command(aliases=['upvote'])
    async def vote(self, ctx):
        """Gimme an upvote if you like me uwu"""
        await ctx.send(f"{ctx.author.mention} Upvoting me here would be greatly appriciated ^w^\nhttps://discordbots.org/bot/365255872181567489/vote")

    @commands.command()
    @commands.cooldown(rate=2, per=900, type=commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion_txt: str):
        """ Send a suggestion to my owner or just tell him hes doing a bad job -w- """
        suggestion = suggestion_txt
        if ctx.guild:
            color = ctx.author.color
            footer = f"Sent from {ctx.guild.name}"
            guild_pic = ctx.guild.icon_url
        else:
            color = 0x254d16
            footer = "Sent from DMs"
            guild_pic = ""
        if len(suggestion) > 2000:
            await ctx.send(f"xwx uhm... {ctx.author.mention} thats a bit too long for me to send. Shorten it and try again. (2000 character limit)")
        else:
            try:
                await ctx.send("alright, i sent your suggestion!! ^w^")
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(os.environ["SUGGESTHOOK"], adapter=AsyncWebhookAdapter(session))
                suggestionem = discord.Embed(description=f"{suggestion}", color=color)
                suggestionem.set_author(name=f"From {ctx.author}", icon_url=ctx.author.avatar_url)
                suggestionem.set_footer(text=footer, icon_url=guild_pic)
                await webhook.send(embed=suggestionem)
            except Exception as e:
                await ctx.send("uhm.. something went wrong, try again later..")
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
        embed.add_field(name="Messages read", value=self.bot.counter["msgs_read"], inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
