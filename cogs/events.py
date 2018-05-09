import discord
import traceback
import datetime

from discord.ext.commands import errors
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from utils import default
from collections import Counter
import os

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


class Events:
    def __init__(self, bot):
        self.bot = bot
        self.counter = Counter()
        self.config = default.get("config.json")

    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = ('{2}\n{0}: {3}').format(type(err).__name__, ctx.message.content, _traceback, err)
            error = error.replace(".heroku", "owo")
            errem = discord.Embed(description=f"{error}")
            await ctx.send(embed=errem)

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.0f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            pass

        elif isinstance(err, errors.NoPrivateMessage):
            await ctx.send("This command can't be used in dms, sowwy.")

    async def on_ready(self):
        info = discord.Embed(title="owopup is online", description=f":small_blue_diamond: Guilds: `{len(self.bot.guilds)}`\n:small_blue_diamond: Users: `{len(set(self.bot.get_all_members()))}`", color=0xf7a836) 
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Users: {len(set(self.bot.get_all_members()))}')
        await self.bot.change_presence(activity=discord.Game(type=0, name="ｏｗｏ"), status=discord.Status.online)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=info)
        
    
    async def on_guild_join(self, guild):
        members = set(guild.members)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send("hewwooo!! ^w^")

        join = discord.Embed(title="Added to Guild ^w^", description=f":small_blue_diamond: | Name: {guild.name}\n:small_blue_diamond: | Members/Bots: {len(guild.members)}\n:small_blue_diamond: | Members/Bots: {len(guild.members)}/{len(bots)}\n:small_blue_diamond: | Owner: {guild.owner}", color=discord.Color.dark_green())
        join.set_thumbnail(url=guild.icon_url)
        join.set_footer(text=f"Total Guilds: {len(self.bot.guilds)}")
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=join)

    async def on_guild_remove(self, guild):
        leave = discord.Embed(title="Removed from Guild umu", description=f":small_blue_diamond: | Name: {guild.name}\n:small_blue_diamond: | Members: {len(guild.members)}\n:small_blue_diamond: | Owner: {guild.owner}", color=discord.Color.dark_red())
        leave.set_thumbnail(url=guild.icon_url)
        leave.set_footer(text=f"Total Guilds: {len(self.bot.guilds)}")
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=leave)
        
def setup(bot):
    bot.add_cog(Events(bot))
