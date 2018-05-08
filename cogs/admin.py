import time
import subprocess
from utils import repo, default, dataIO
from utils.chat_formatting import pagify
from discord.ext import commands
import os
import asyncio
import discord
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

async def run_cmd(cmd: str) -> str:
    """Runs a subprocess and returns the output."""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)

class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

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
        """ Reloads an extension. """
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

    @commands.command(aliases=['exec'])
    @commands.check(repo.is_owner)
    async def execute(self, ctx, *, text: str):
        """ Do a shell command. """
        try:
            text_parsed = list(filter(None, text.split(" ")))
            output = subprocess.check_output(text_parsed).decode()
            await ctx.send(f"```fix\n{output}\n```")
        except Exception as e:
            await ctx.send(f"```fix\n{e}\n```")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def debug(self, ctx, *, command: str):
        """Run stuff"""
        with ctx.typing():
            await run_cmd('git init')
            await run_cmd('git remote add pup https://github.com/Skullbite/uwupup') # just in case git wants to be an ass.
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
        info = discord.Embed(description=f"ｏｗｏ```py\n{pull}```", color=0x00695c)
        msg = await ctx.send(embed=info, delete_after=20)
        
    @commands.command()
    @checks.is_owner()
    async def servers(self, ctx):
        """Lists and allows to leave servers"""
        owner = ctx.author
        guilds = sorted(list(self.bot.guilds),
                        key=lambda s: s.name.lower())
        msg = ""
        for i, server in enumerate(guilds, 1):
            msg += "{}: {}\n".format(i, server.name)

        msg += "\nTo leave a server, just type its number."

        for page in pagify(msg, ['\n']):
            await ctx.send(page)
  
    @commands.command()
    @commands.check(repo.is_owner)
    async def whtest(self, ctx, whlink: str):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(f'{whlink}', adapter=AsyncWebhookAdapter(session))
            await webhook.send("hewwo?")
    
                
def setup(bot):
    bot.add_cog(Admin(bot))
