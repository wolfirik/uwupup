import time
import subprocess
from utils import repo, default, dataIO
from utils.chat_formatting import pagify, box
from discord.ext import commands
import os
import asyncio
import discord
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from contextlib import redirect_stdout
from copy import copy
import inspect
import textwrap
import sqlite3
import rethinkdb as r
import psutil

async def run_cmd(cmd: str) -> str:
    """Runs a subprocess and returns the output."""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)

port = int(os.environ['PORT'])

class Admin:
    def __init__(self, bot):
        self.bot = bot
        #self.conn = r.connect(host='uwupup.herokuapp.com', port=port, timeout=30)
        self.config = default.get("config.json")
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(e):
        """Format a syntax error to send to the user.
        Returns a string representation of the error formatted as a codeblock.
        """
        if e.text is None:
            return box('{0.__class__.__name__}: {0}'.format(e), lang="py")
        return box(
            '{0.text}{1:>{0.offset}}\n{2}: {0}'
            ''.format(e, '^', type(e).__name__),
            lang="py")


    def get_pages(msg: str):
        """Pagify the given message for output to the user."""
        return pagify(msg, delims=["\n", " "], priority=True, shorten_by=10)


    def sanitize_output(ctx: commands.Context, input_: str) -> str:
        """Hides the bot's token from a string."""
        token = ctx.bot.http.token
        r = "were you expecting a tyoken..?"
        result = input_.replace(token, r)
        result = result.replace(token.lower(), r)
        result = result.replace(token.upper(), r)
        return result

    @commands.command()
    async def amiadmin(self, ctx):
        """ Are you admin? """
        if ctx.author.id in repo.owners:
            return await ctx.send(f"Yes **{ctx.author.name}** you are admin! ✅")

        # Please do not remove this part.
        # I would love to be credited as the original creator of the source code.
        if ctx.author.id == 86477779717066752:
            return await ctx.send(f"Well kinda **{ctx.author.name}**.. you still own the source code")

        await ctx.send(f"no, heck off {ctx.author.name}")

    @commands.command(aliases=['re'])
    @commands.check(repo.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            await ctx.send(f"```\n{e}```")
            return
        await ctx.send(f"Reloaded extension **{name}** ^w^")

    @commands.command()
    @commands.check(repo.is_owner)
    async def reboot(self, ctx):
        """ Reboot the bot """
        await ctx.send('Rebooting now...')
        time.sleep(1)
        await self.bot.logout()

    @commands.command()
    @commands.check(repo.is_owner)
    async def load(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            await ctx.send(f"```diff\n- {e}```")
            return
        await ctx.send(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.check(repo.is_owner)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        if name == "admin":
            ctx.send("prolly not a good idea to unload this. don't ya think..?")
            return
        else:
            try:
                self.bot.unload_extension(f"cogs.{name}")
            except Exception as e:
                await ctx.send(f"```diff\n- {e}```")
                return
            await ctx.send(f"Unloaded extension **{name}.py**")

    @commands.group()
    @commands.check(repo.is_owner)
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @change.command(name="playing")
    @commands.check(repo.is_owner)
    async def change_playing(self, ctx, *, playing: str):
        """ Change playing status. """
        try:
            await self.bot.change_presence(
                activity=discord.Game(type=0, name=playing),
                status=discord.Status.online
            )
            dataIO.change_value("config.json", "playing", playing)
            await ctx.send(f"Successfully changed playing status to **{playing}**")
        except discord.InvalidArgument as err:
            await ctx.send(err)
        except Exception as e:
            await ctx.send(e)

    @change.command(name="username")
    @commands.check(repo.is_owner)
    async def change_username(self, ctx, *, name: str):
        """ Change username. """
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(err)

    @change.command(name="nickname")
    @commands.check(repo.is_owner)
    async def change_nickname(self, ctx, *, name: str = None):
        """ Change nickname. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"Successfully changed nickname to **{name}**")
            else:
                await ctx.send("Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)

    @change.command(name="avatar")
    @commands.check(repo.is_owner)
    async def change_avatar(self, ctx, url: str = None):
        """ Change avatar. """
        if url is None and len(ctx.message.attachments) == 1:
            url = ctx.message.attachments[0].url
        else:
            url = url.strip('<>')

        try:
            bio = await http.get(url, res_method="read")
            await self.bot.user.edit(avatar=bio)
            await ctx.send(f"Successfully changed the avatar. Currently using:\n{url}")
        except aiohttp.InvalidURL:
            await ctx.send("The URL is invalid...")
        except discord.InvalidArgument:
            await ctx.send("This URL does not contain a useable image")
        except discord.HTTPException as err:
            await ctx.send(err)

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def debug(self, ctx, *, command: str):
        """Run stuff"""
        with ctx.typing():
            await run_cmd('git init')
            await run_cmd('git remote add pup https://github.com/Skullbite/uwupup') # just in case git wants to be an ass.
            await run_cmd(f'git config --globsl user.email "{os.environ["EMAIL"]}"')
            await run_cmd(f'git config --global user.name "Skullbite"')
            result = await run_cmd(command)
            em = discord.Embed(description=f"```fix\n{result}\n```", color=0x00695c)
            if len(result) >= 1500:
                await ctx.send(f'wew. {command} has a big output.. i-i\'ll print it instead..')
                print(result)
            else:
                await ctx.send(embed=em)

    @commands.command(hidden=True, aliases=["pull"])
    @commands.check(repo.is_owner)
    async def update(self, ctx):
        """gets latest commits and applies them from git"""
        await run_cmd('git init')
        await run_cmd('git remote add pup https://github.com/Skullbite/uwupup')
        pull = await run_cmd('git pull pup master --no-commit --no-edit --ff-only')
        await run_cmd('git fetch --all')
        ack = await run_cmd('git reset --hard pup/master')
        pull = pull.replace('https://github.com/Skullbite/uwupup', 'owopup')
        info = discord.Embed(description=f"ｏｗｏ:fast_forward: ```py\n{pull}```", color=0x254d16)
        msg = await ctx.send(embed=info, delete_after=6)
        
    @commands.command()
    @commands.check(repo.is_owner)
    async def servers(self, ctx):
        """Lists servers"""
        owner = ctx.author
        guilds = sorted(list(self.bot.guilds),
                        key=lambda s: s.name.lower())
        msg = ""
        for i, server in enumerate(guilds, 1):
            msg += "`{}:` {}\n".format(i, server.name)

        for page in pagify(msg, ['\n']):
            await ctx.send(page)

    @commands.command()
    @commands.check(repo.is_owner)
    async def eval(self, ctx, *, code):
        """Evaluate a statement of python code.
        Environment Variables:
            ctx      - command invokation context
            bot      - bot object
            channel  - the current channel object
            author   - command author's member object
            message  - the command's message object
            discord  - discord.py library
            commands - discord.py commands extension
            _        - The result of the last dev command.
        """
        env = {
            'bot': ctx.bot,
            'ctx': ctx,
            'ps': psutil,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'discord': discord,
            'commands': commands,
            '_': self._last_result
        }

        code = self.cleanup_code(code)

        try:
            result = eval(code, env)
        except SyntaxError as e:
            await ctx.send(self.get_syntax_error(e))
            return
        except Exception as e:
            await ctx.send('{}: {!s}'.format(type(e).__name__, e))
            return

        if asyncio.iscoroutine(result):
            result = await result

        self._last_result = result
        result = self.sanitize_output(result)

        try:
            await ctx.send(f"{result}")
        except:
            print(result)
            await ctx.send("it was too long so i just printed it.")

    @commands.command()
    @commands.check(repo.is_owner)
    async def whtest(self, ctx, whlink: str):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(f'{whlink}', adapter=AsyncWebhookAdapter(session))
            await webhook.send("hewwo?")
    
    @commands.command()
    @commands.check(repo.is_owner)
    async def gsi(self, ctx, *, guild_id: str):
        """ Makes me get the information from a guild id"""
        guild = self.bot.get_guild(guild_id)
        try:
            guild = self.bot.get_guild(guild_id)
            members = set(guild.members)
            bots = filter(lambda m: m.bot, members)
            bots = set(bots)
            info = discord.Embed(title="Guild info", description=f":small_blue_diamond: | Name: {guild.name}\n:small_blue_diamond: | Members/Bots: {len(guild.members)}\n:small_blue_diamond: | Members/Bots: {len(guild.members)}/{len(bots)}\n:small_blue_diamond: | Owner: {guild.owner}", color=discord.Color.blue())
            info.set_thumbnail(url=guild.icon_url)
            ctx.send(embed=info)
        except:
            ctx.send("Hmmph i got nothin. Either you gave an invalid server id or i'm not in that server")

    @commands.command()
    @commands.check(repo.is_owner)
    async def rethink(self, ctx, *, thing: str):
        this = r.db_create(f"{thing}").run(self.conn)
        await ctx.send(f"saved `{thing}` to rethink\n Output: {this}")

    @commands.command()
    @commands.check(repo.is_owner)
    async def recall(self, ctx): 
        await ctx.send("oof")

    @commands.command()
    @commands.check(repo.is_owner)
    async def cogs(self, ctx):
        mod = ", ".join(list(self.bot.cogs))
        await ctx.send(f"The current modules I can see are:\n{mod}")

def setup(bot):
    bot.add_cog(Admin(bot))
