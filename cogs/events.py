import discord
import traceback
import datetime

from discord.ext.commands import errors
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from utils import default
from collections import Counter
import os
from datetime import datetime
import dbl

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
        self.token = os.environ["DBL_TOKEN"] 
        self.dblpy = dbl.Client(self.bot, self.token, loop=bot.loop)
        self.updating = bot.loop.create_task(self.update_stats())

    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_cmd_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = ('{}:\n {}').format(type(err).__name__, err)
            error = error.replace(".heroku", "owo")
            errem = discord.Embed(description=f"{error}")
            await ctx.send(embed=errem)

        elif isinstance(err, errors.CheckFailure):
            no = self.bot.get_emoji(315009174163685377)
            try:
                await ctx.message.add_reaction(no)
            except:
                await ctx.send("either you're in the wrong channel or you don't have perms to use this command :thinking:")

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.0f} seconds.")

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
        await self.bot.change_presence(activity=discord.Game(type=0, name=os.environ["PLAYING"]), status=discord.Status.online)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=info)
        
    
    async def on_guild_join(self, guild):
        members = set(guild.members)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        members = len(members) - len(bots)
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send("hewwooo!! ^w^")

        if len(bots) > len(guild.members):
            sketchy_msg = "\n<:blobdoggothink:444122378260185088> | **Prolly a bot farm or bot testing guild**"
        else: 
            sketchy_msg = ""

        join = discord.Embed(title="Added to Guild ^w^", description=f":small_blue_diamond: | Name: {guild.name}\n:small_blue_diamond: | Members/Bots: `{members}:{len(bots)}`\n:small_blue_diamond: | Owner: {guild.owner}{sketchy_msg}", color=discord.Color.dark_green())
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

    async def update_stats(self):
        update = discord.Embed(title="Updating Server Count",  description="<a:dblspin:393548363879940108> Posted {} Guilds".format(len(self.bot.guilds)), color=discord.Color.blurple()) 
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
        while True:
            print('Attempting to post server count')
            try:
                await aiohttp.ClientSession().post('https://discordbots.org/api/bots/' + str(self.bot.user.id) + '/stats', json={"server_count": len(self.bot.guilds)}, headers={'Authorization': os.environ["DBL_TOKEN"] })
                await webhook.send(embed=update)
            except Exception as e:
                try: #if the webhook is online
                    err = discord.Embed(description=f"failed to post owo's server count, sowwy.\n{type(e).__name__}```{e}```", color=discord.Color.red())
                    await webhook.send(embed=err)
                except: #if not... 
                    print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

        
def setup(bot):
    bot.add_cog(Events(bot))
