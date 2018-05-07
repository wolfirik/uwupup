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
        time = datetime.now(EST)
        info = discord.Embed(title="owopup is online", description=f"Guilds: `{len(self.bot.guilds)}`\nUsers: `{len(set(self.bot.get_all_members()))}`")
        info.set_footer(text=f"Booted at: {time}")
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Users: {len(set(self.bot.get_all_members()))}')
        await self.bot.change_presence(activity=discord.Game(type=0, name="ｏｗｏ"), status=discord.Status.online)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send("owo has successfully booted, i think")
        
    
    async def on_guild_join(guild):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send("owopup has been added to {guild.name}\nTotal Guilds: {len(self.bot.guilds)}")
        
def setup(bot):
    bot.add_cog(Events(bot))
