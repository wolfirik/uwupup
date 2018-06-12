import time
import datetime
import subprocess
from utils import repo, default, dataIO, http
from utils.chat_formatting import pagify, box
from discord.ext import commands
from copy import deepcopy
import os
import asyncio
import discord
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from contextlib import redirect_stdout
from copy import copy
import inspect
import textwrap
import psutil
import requests
import psycopg2
from io import BytesIO
from pymongo import MongoClient
import json

async def run_cmd(cmd: str) -> str:
    """Runs a subprocess and returns the output."""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)

db_uri = os.environ['MONGOLAB_NAVY_URI']

class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client['owopup']
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
    async def post(self, ctx):
        dbltoken = os.environ["DBL_TOKEN"]
        pwtoken = os.environ["PW_TOKEN"]
        dblemote = self.bot.get_emoji(338808864352763904)
        pwemote = self.bot.get_emoji(230104938858938368)
        urldbl = "https://discordbots.org/api/bots/365255872181567489/stats"
        urlpw = "https://bots.discord.pw/api/bots/365255872181567489/stats"
        headersdbl = {"Authorization" : dbltoken}
        headerspw = {"Authorization" : pwtoken}
        yup = self.bot.get_emoji(451741018425917440)
        nope = self.bot.get_emoji(451741018539163648)
        try:
            payloaddbl = {"server_count"  : len(self.bot.guilds)}
            payloadpw = {
                            "server_count": len(self.bot.guilds)
                        } #json's formatted differently.
            dbl = requests.post(urldbl, data=payloaddbl, headers=headersdbl)
            pw = requests.post(urlpw, data=payloadpw, headers=headerspw)
            dbl = dbl.json()
            pw = pw.json()
            await ctx.send(f"{dblemote} `{dbl}`\n{pwemote} `{pw}`")
            await ctx.message.add_reaction(yup)
        except Exception as e:
            await ctx.send(e)
            await ctx.message.add_reaction(nope)

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
            await ctx.send("prolly not a good idea to unload this. don't ya think..?")
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
        yup = self.bot.get_emoji(451741018425917440)
        pull = await run_cmd('git pull pup master --no-commit --no-edit --ff-only')
        await run_cmd('git fetch --all')
        ack = await run_cmd('git reset --hard pup/master')
        pull = pull.replace('https://github.com/Skullbite/uwupup', 'owopup')
        info = discord.Embed(description=f"ｏｗｏ:fast_forward: ```css\n{pull}```", color=0x254d16)
        info2 = discord.Embed(description=f"{yup} pull complete uwu", color=0x254d16)
        msg = await ctx.send(embed=info)
        time.sleep(6)
        await msg.edit(embed=info2)

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
            'requests': requests,
            'db': self.db,
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
        if code == "bot.http.token":
            f = "HA GOTEEM"
            memes = BytesIO(f.encode('utf-8'))
            await ctx.send(content="Here you go", file=discord.File(memes, filename="eval.txt"))

        else:
            try:
                await ctx.send(f"{result}")
            except:
                f = f"{result}"
                memes = BytesIO(f.encode('utf-8'))
                await ctx.send("Output's too big heres the file.", file=discord.File(memes, filename='eval.txt'))

    @commands.command()
    @commands.check(repo.is_owner)
    async def whtest(self, ctx, whlink: str):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(f'{whlink}', adapter=AsyncWebhookAdapter(session))
            await webhook.send("hewwo?")

    @commands.command()
    @commands.check(repo.is_owner)
    async def gsi(self, ctx, *, guild_id: int):
        """ Makes me get the information from a guild id"""
        guild = self.bot.get_guild(guild_id)
        try:
            members = set(guild.members)
            bots = filter(lambda m: m.bot, members)
            bots = set(bots)
            members = len(members) - len(bots)
            if guild == ctx.guild:
                roles = ", ".join([x.mention for x in guild.roles])
            else:
                roles = "oof"

            info = discord.Embed(title="Guild info", description=f":small_blue_diamond: | Name: {guild.name}\n:small_blue_diamond: | Members/Bots: {members}/{len(bots)}"
                                                                  f"\n:small_blue_diamond: | Owner: {guild.owner}\n:small_blue_diamond: | Created at: {guild.created_at}"
                                                                  f"\n:small_blue_diamond: | Roles: {roles}"
                                                                  f"\n:small_blue_diamond: | Shard ID (useless rn): {guild.shard_id}", color=discord.Color.blue())
            info.set_thumbnail(url=guild.icon_url)
            await ctx.send(embed=info)
        except:
            await ctx.send("Hmmph i got nothin. Either you gave an invalid server id or i'm not in that server")

    @commands.command()
    @commands.check(repo.is_owner)
    async def mongo(self, ctx):
        post_data = [{ 'name' : "jeff", 'meme': "null" }]
        #post_data = json.loads(post_data)
        headers = {'content-type': 'application/json'}
        r = requests.post(f'https://api.mlab.com/api/1/databases/{os.environ["DB_NAME"]}/collections/test?apiKey={os.environ["MLAB_KEY"]}', data=post_data, headers=headers)
        r = r.json()
        await ctx.send(r)

    @commands.command()
    @commands.check(repo.is_owner)
    async def recall(self, ctx):
        r = requests.get(f'https://api.mlab.com/api/1/databases/{os.environ["DB_NAME"]}/collections/test/5b158cf5e7179a6034c6fd69?apiKey={os.environ["MLAB_KEY"]}')
        r = r.json()
        await ctx.send(r)

    @commands.command()
    @commands.check(repo.is_owner)
    async def mon(self, ctx):
        r = requests.get(f'https://api.mlab.com/api/1/databases?apiKey={os.environ["MLAB_KEY"]}')
        r = r.json()
        await ctx.send(r)

    @commands.command()
    @commands.check(repo.is_owner)
    async def cogs(self, ctx):
        mod = ", ".join(list(self.bot.cogs))
        await ctx.send(f"The current modules I can see are:\n{mod}")

    async def on_ready(self):
        await run_cmd('git init')
        await run_cmd('git remote add pup https://github.com/Skullbite/uwupup')
        await run_cmd('git pull pup master --no-commit --no-edit --ff-only')

def setup(bot):
    bot.add_cog(Admin(bot))
