import time
import discord
import psutil
import os

from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from datetime import datetime
from utils import repo, default, http
from io import BytesIO
import requests


class Information:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.color = 0x254d16
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
    @commands.check(repo.is_owner)
    async def fakehelp(self, ctx, *, commands : str=None):
        if not commands:
            help = await self.bot.formatter.format_help_for(ctx, self.bot)
            try:
                for page in help:
                    page = page.replace("```", "`")
                    page = discord.Embed(description=page, color=0x254d16)
                    await ctx.author.send(embed=page)
                    await ctx.send("Alright, Sent! uwu")
            except discord.Forbidden:
                return await ctx.send("ack, do you have dms disabled or something..?")
        else:
            try:
                cmd_help = await self.bot.formatter.format_help_for(ctx, commands)
                await ctx.send(cmd_help)
            except:
                await ctx.send("ack, i couldn't find that command")

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!\n`MSG :: {int(ping)}ms\nAPI :: {round(self.bot.latency * 1000)}ms`")

    @commands.command(aliases=['joinme', 'links', 'botinvite'])
    async def invite(self, ctx):
        """ Invite me to your server """
        server = self.bot.get_emoji(314003252830011395)
        bottag = self.bot.get_emoji(230105988211015680)
        invite = discord.Embed(title="Bot links", description=f"{bottag} [**Bot Invite**](https://discordapp.com/oauth2/authorize?client_id=365255872181567489&scope=bot&permissions=470150214)\n{server} [**Support Guild Invite**](https://discord.gg/c4vWDdd)", color=0x254d16)
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
            suggestionem = discord.Embed(description=f"{suggestion}", color=color)
            suggestionem.set_author(name=f"From {ctx.author}", icon_url=ctx.author.avatar_url)
            suggestionem.set_footer(text=footer, icon_url=guild_pic)
            try:
                await ctx.send("Alright, i sent your suggestion!! ^w^")
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(os.environ["SUGGESTHOOK"], adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=suggestionem)
            except Exception as e:
                return await ctx.send("uhm.. something went wrong, try again later..")
    
    @commands.group()
    async def dbl(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                r = discord.Embed(description=page.replace("```", "`"), color=self.color)
                await ctx.send(embed=r)
                
    @dbl.command(name="widget", aliases=["w"])
    async def dbl_widget(self, ctx, botto: discord.Member):
        """Generates a discordbots.org widget"""
        if not botto.bot:
            return await ctx.send(f'Wow, passing off a user as a bot, you\'re a fuckin\' genius {ctx.author.mention}')
        elif botto == self.bot.user:
            link = f"https://discordbots.org/api/widget/365255872181567489.png?topcolor=2b5a19&middlecolor=32681e&datacolor=ffffff&highlightcolor=254d16&labelcolor=ffffff&certifiedcolor=0d94ba"
            thing = BytesIO(await http.get(link, res_method="read"))
            with ctx.typing():
                try:
                    await ctx.send(file=discord.File(thing, filename="dbl.png"))
                except:
                    await ctx.send("oof")
        else:
            try:
                with ctx.typing():
                    color = botto.color
                    link = f"https://discordbots.org/api/widget/{botto.id}.png?topcolor={color}&datacolor=ffffff&highlightcolor={color}&labelcolor=ffffff&certifiedcolor=0d94ba".replace("#", "")
                    thing = BytesIO(await http.get(link, res_method="read"))
                    await ctx.send(file=discord.File(thing, filename="dbl.png"))
            except discord.Forbidden:
                await ctx.send("Can i even send pics?")
            except Exception as e:
                await ctx.send(e)
                
    @dbl.command(name="info", aliases=["i"])
    async def dbl_info(self, ctx, bot: discord.Member):
        """Gets a bot's info from discordbots.org"""
        if not bot.bot:
            pass
        else:
            base = requests.get(f"https://discordbots.org/api/bots/{bot.id}").json()
            emote = self.bot.get_emoji(393548363879940108)
            prefix = base.get("prefix")
            cert = base.get("certifiedBot")
            if cert == False:
                cert = "Nyope, i don't think so..."
            else:
                cert = "Uhhhh Yes!"
            tags = ", ".join(base.get("tags"))
            points = base.get("points")
            desc = base.get("shortdesc")
            owners = list(base.get("owners"))
            
            for owner in owners:
                owners = self.bot.get_user(int(owner))
            m = discord.Embed(description=f"```{desc}```\nTotal Votes: {points}\nPrefix: {prefix}\nTags: {tags}\nCertified? `{cert}`", color=self.color)
           # m.set_footer(text=f"Primary Owner: {owners}", icon_url=owners.avatar_url)
            m.set_author(name=f"DBL stats for {bot}", icon_url=emote.url)
            m.set_thumbnail(url=bot.avatar_url)
            await ctx.send(embed=m)
            
                
    @commands.command(aliases=["lc"])
    async def lcord(self, ctx, bot: discord.Member):
        """Gets a bots info from listcord"""
        if not bot.bot:
            return await ctx.send(f'Wow, passing off a user as a bot, you\'re a fuckin\' genius {ctx.author.mention}')
        else:
            base = requests.get(f"https://listcord.com/api/bot/{bot.id}").json()
            if base.get("code") == 0:
                return await ctx.send("uhhhhhh I couldn't find that bot.")
            else:
                emote = self.bot.get_emoji(462350611854262282)
                b = requests.get(f"https://listcord.com/api/bot/{bot.id}").json()
                desc = b.get("description")
                prefix = b.get("prefix")
                invites = b.get("invites")
                owners = " ".join(b.get("owners"))
                upvotes = b.get("votes")
                invite = b.get("invite")
                em = discord.Embed(description=f"Bot Description:```{desc}```\n\nPrefix: `{prefix}`\nInvites: `{invites}`\nUpvotes: `{upvotes}`\n[Bot Invite]({invite})\n[Bot Page](https://listcord.com/bot/{bot.id})", color=self.color)
                em.set_author(name=f"Listcord stats for {bot}", icon_url=emote.url)
                em.set_thumbnail(url=bot.avatar_url)
                em.set_image(url=f"https://nuggetbot.com/listcord/embed.png?id={bot.id}")
                em.set_footer(text=f"", icon_url="")
                await ctx.send(embed=em)
            
    @commands.command()
    async def source(self, ctx):
        """ Credits """
        await ctx.send(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/xelA/discord_bot.py")

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        color = 0x79589F
        owner = self.bot.get_user(158750488563679232)

        embed = discord.Embed(colour=color)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Uptime", value=self.get_bot_uptime(), inline=False)
        embed.add_field(name="Dev", value=owner, inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=len(ctx.bot.guilds), inline=True)
        embed.add_field(name="Commands used", value=self.bot.counter["cmds_ran"], inline=True)
        embed.add_field(name="Messages read", value=self.bot.counter["msgs_read"], inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.set_footer(text="Heroku Version")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
