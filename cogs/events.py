import discord
import traceback
import datetime

from discord.ext.commands import errors
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from utils import default, permissions, emotes
from collections import Counter
import os
from datetime import datetime
import requests
from utils.http2 import krequest as kr
import asyncio

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        page = page.replace("```", "`") # TODO: Stop being lazy and write a custom help command.
        page = discord.Embed(description=page, color=0x254d16)
        await ctx.send(embed=page)


class Events:
    def __init__(self, bot):
        self.bot = bot
        self.counter = Counter()
        self.config = default.get("config.json")
        self.bot.loop.create_task(self.uptimer())


    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = ('{}:\n{}').format(type(err).__name__, err)
            error = error.replace(".heroku", "owo")
            errem = discord.Embed(title="error occured!", description=f"{error}")
            await ctx.send(embed=errem)

        elif isinstance(err, errors.CheckFailure):
            no = self.bot.get_emoji(451741018539163648)
            try:
                await ctx.message.add_reaction(no)
            except:
                await ctx.send("either you're in the wrong channel or you don't have perms to use this command :thinking:")

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"aaa..! i f-feel kinda dizzy... pl-please try again in {err.retry_after:.0f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

        elif isinstance(err, errors.NoPrivateMessage):
            await ctx.send("This command can't be used in dms, sowwy.")

    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()
        info = discord.Embed(title=f"{self.bot.user} is online", description=f":small_blue_diamond: Guilds: `{len(self.bot.guilds)}`\n:small_blue_diamond: Users: `{len(set(self.bot.get_all_members()))}`", color=0xf7a836)
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Users: {len(set(self.bot.get_all_members()))}')
        print(f'\nCogs Loaded: {", ".join(list(self.bot.cogs))}')
        await self.bot.change_presence(activity=discord.Game(type=0, name=f"noticing bulges in {len(self.bot.guilds)} servers >w> | owo help"), status=discord.Status.online)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=info)


    async def on_guild_join(self, guild):
        members = set(guild.members)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        members = len(members) - len(bots)
        dbltoken = os.environ["DBL_TOKEN"]
        pwtoken = os.environ["PW_TOKEN"]
        urldbl = "https://discordbots.org/api/bots/365255872181567489/stats"
        urlpw = f"https://bots.discord.pw/api/bots/{self.bot.user.id}/stats"
        urllcord = f"https://listcord.com/api/bot/{self.bot.user.id}/guilds"
        dblemote = self.bot.get_emoji(338808864352763904)
        pwemote = self.bot.get_emoji(230104938858938368)
        payload = {"server_count"  : len(self.bot.guilds)}
        logs = self.bot.get_channel(433476786597265409)
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
            try:
                invite_chan = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).create_instant_invite and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
                invite = await invite_chan.create_invite(reason="Don't mind me")
            except:
                invite_msg = "**Invite Unavailable**"
        except IndexError:
            pass
        else:
            pass
            invite_msg = f"[**Guild Invite**]({invite})"
        if len(bots) > members:
            sketchy_msg = "\n<:blobdoggothink:444122378260185088> **More Bots than users**"
        else:
            sketchy_msg = ""

        join = discord.Embed(title="Added to Guild ^w^", description=f"» Name: {guild.name}\n» ID: {guild.id}\n» Reigion: {guild.region}\n» Members/Bots: `{members}:{len(bots)}`\n» Owner: {guild.owner}{sketchy_msg}\n» {invite_msg}", color=discord.Color.dark_green())
        join.set_thumbnail(url=guild.icon_url)
        join.set_footer(text=f"Total Guilds: {len(self.bot.guilds)}")
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=join)
        dbl = await kr().post(urldbl, headers={"Authorization": dbltoken}, data=payload)
        pw = await kr().post(urlpw, headers={"Authorization": pwtoken}, data=payload)
        lcord = await kr().post(urllcord, headers={"Authorization": lcordtoken}, data={"guilds": len(self.bot.guilds)})
        stats = discord.Embed(description=f"{dblemote} {dbl}\n{pwemote} `{pw}`")
        await logs.send(embed=stats) 

    async def on_guild_remove(self, guild):
        members = set(guild.members)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        members = len(members) - len(bots)
        dbltoken = os.environ["DBL_TOKEN"]
        pwtoken = os.environ["PW_TOKEN"]
        urldbl = "https://discordbots.org/api/bots/365255872181567489/stats"
        urlpw = "https://bots.discord.pw/api/bots/365255872181567489/stats"
        payload = {"server_count"  : len(self.bot.guilds)}
        leave = discord.Embed(title="Removed from Guild umu", description=f"» Name: {guild.name}\n» ID: {guild.id}\n» Region: {guild.region}\n» Members/Bots: `{members}:{len(bots)}`\n» Owner: {guild.owner}", color=discord.Color.dark_red())
        leave.set_thumbnail(url=guild.icon_url)
        leave.set_footer(text=f"Total Guilds: {len(self.bot.guilds)}")
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=leave)

    async def on_message(self, msg):
        self.bot.counter["msgs_read"] += 1
    
    async def on_message_edit(self, before, after):
        if not self.bot.is_ready() or after.author.bot or not permissions.can_send(after):
            return

        await self.bot.process_commands(after)
        self.bot.counter["cmds_ran"] += 1
        
    async def on_resumed(self):
        self.bot.counter["sessions_resumed"] += 1
        
    async def uptimer(self):
        while True:
            print("a")
            await asyncio.sleep(240)


def setup(bot):
    bot.add_cog(Events(bot))
