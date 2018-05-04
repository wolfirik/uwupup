import discord
import traceback

from discord.ext.commands import errors
from utils import default
from collections import Counter

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
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Users: {len(set(self.bot.get_all_members()))}')
        await self.bot.change_presence(activity=discord.Game(type=0, name="ｏｗｏ"), status=discord.Status.online)
    
        
def setup(bot):
    bot.add_cog(Events(bot))
