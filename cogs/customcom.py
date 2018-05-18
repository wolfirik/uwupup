import re

import discord
import rethinkdb as r
from __main__ import send_cmd_help
from discord.ext import commands

from .utils import checks
from .utils.chat_formatting import pagify


class CustomCommands:
    """Custom commands

    Creates commands used to display text"""

    def __init__(self, bot):
        self.bot = bot

    async def check_settings(self, guild):
        t = await r.table('guilds').get(str(guild.id)).run(self.bot.conn)
        if "commands" not in t:
            t["commands"] = []
            await r.table('guilds').insert(t, conflict="update").run(self.bot.conn)

    @commands.group(aliases=["cc"], pass_context=True, no_pm=True)
    async def customcom(self, ctx):
        """Custom commands management"""
        await self.check_settings(ctx.guild)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @staticmethod
    async def load_coms(guildid: str, bot):
        loaded = await r.table("guilds").get(guildid).run(bot.conn)
        if loaded is None or "commands" not in loaded:
            return {}
        return loaded["commands"]

    @staticmethod
    async def save_coms(guildid: str, ncommands: dict):
        a = await r.connect(host="localhost", port=28015, db='fur')
        await r.table("guilds").update({"commands": ncommands}, conflict="replace").run(a)

    @customcom.command(name="add", pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def cc_add(self, ctx, command: str, *, text):
        """Adds a custom command

        Example:
        [p]cc add yourcommand Text you want
        """
        await self.check_settings(ctx.guild)
        guild = ctx.message.guild
        command = command.lower()
        if command in self.bot.commands:
            desc = "That command is already a standard command."
            em = discord.Embed(description=desc, color=0xFF0000)
            await ctx.send(embed=em)
            return
        cmdlist = await self.load_coms(str(guild.id), self.bot)
        if command not in cmdlist:
            cmdlist[command] = text
            await self.save_coms(str(guild.id), cmdlist)
            desc = "Custom command successfully added."
            em = discord.Embed(description=desc, color=self.bot.color)
            await ctx.send(embed=em)
        else:
            desc = "This command already exists. Use `furcustomcom edit` to edit it."
            em = discord.Embed(description=desc, color=self.bot.color)
            await ctx.send(embed=em)

    @customcom.command(name="edit", pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def cc_edit(self, ctx, command: str, *, text):
        """Edits a custom command

        Example:
        [p]customcom edit yourcommand Text you want
        """
        guild = ctx.message.guild
        command = command.lower()
        cmdlist = await self.load_coms(str(guild.id), self.bot)
        if not cmdlist:
            desc = "There are no custom commands in this guild. Use `furcustomcom add` to start adding some."
            em = discord.Embed(description=desc, color=0xFF0000)
            await ctx.send(embed=em)
            return
        if command in cmdlist:
            cmdlist[command] = text
            await self.save_coms(str(guild.id), cmdlist)
            desc = "Custom command successfully edited."
            em = discord.Embed(description=desc, color=self.bot.color)
            await ctx.send(embed=em)
        else:
            desc = "That command doesn't exist. Use `furcustomcom add` to add it."
            em = discord.Embed(description=desc, color=self.bot.color)
            await ctx.send(embed=em)

    @customcom.command(name="delete", pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def cc_delete(self, ctx, command: str):
        """Deletes a custom command
        Example:
        [p]customcom delete yourcommand"""
        await self.check_settings(ctx.guild)
        guild = ctx.message.guild
        command = command.lower()
        cmdlist = await self.load_coms(str(guild.id), self.bot)
        if not cmdlist:
            desc = "There are no custom commands in this guild. Use `furcustomcom add` to start adding some."
            em = discord.Embed(description=desc, color=0xFF0000)
            await ctx.send(embed=em)
            return
        if command in cmdlist:
            del cmdlist[command]
            await self.save_coms(str(guild.id), cmdlist)
            desc = "Custom command successfully deleted."
            em = discord.Embed(description=desc, color=self.bot.color)
            await ctx.send(embed=em)
        else:
            desc = "That command doesn't exist."
            em = discord.Embed(description=desc, color=0xFF0000)
            await ctx.send(embed=em)

    @customcom.command(name="list", pass_context=True)
    async def cc_list(self, ctx):

        """Shows custom commands list"""
        await self.check_settings(ctx.guild)
        guild = ctx.message.guild
        ccommands = await self.load_coms(str(guild.id), self.bot)
        if not ccommands:
            desc = "There are no custom commands in this guild. Use `customcom add` to start adding some."
            em = discord.Embed(description=desc, color=0xFF0000)
            await ctx.send(embed=em)
            return

        ccommands = ", ".join([ctx.prefix + c for c in sorted(ccommands)])

        if len(ccommands) < 1500:
            desc = ccommands
            em = discord.Embed(description=desc, color=self.bot.color)
            em.set_author(name='Custom Commands:')
            await ctx.send(embed=em)
        else:
            for page in pagify(ccommands, delims=[" ", "\n"]):
                desc = page
                em = discord.Embed(description=desc, color=self.bot.color)
                em.set_author(name='Custom Commands:')
                await self.bot.whisper(embed=em)


    async def on_message(self, message):
        if len(message.content) < 2 or isinstance(message.channel, discord.abc.PrivateChannel):
            return

        guild = message.guild
        prefix = message.prefix
        if not prefix:
            return
        if not message.content.startswith(prefix):
            return
        cmdlist = await self.load_coms(str(guild.id), self.bot)
        if cmdlist and not message.author.bot:
            cmd = message.content[len(prefix):]
            if cmd in cmdlist:
                cmd = cmdlist[cmd]
                cmd = self.format_cc(cmd, message)
                await message.channel.send(cmd)
            elif cmd.lower() in cmdlist:
                cmd = cmdlist[cmd.lower()]
                cmd = self.format_cc(cmd, message)
                await message.channel.send(cmd)

    def format_cc(self, command, message):
        results = re.findall("{([^}]+)}", command)
        for result in results:
            param = self.transform_parameter(result, message)
            command = command.replace("{" + result + "}", param)
        return command

    @staticmethod
    def transform_parameter(result, message):
        """
        For security reasons only specific objects are allowed
        Internals are ignored
        """
        raw_result = "{" + result + "}"
        objects = {
            "message": message,
            "author": message.author,
            "channel": message.channel,
            "guild": message.guild
        }
        if result in objects:
            return str(objects[result])
        try:
            first, second = result.split(".")
        except ValueError:
            return raw_result
        if first in objects and not second.startswith("_"):
            first = objects[first]
        else:
            return raw_result
        return str(getattr(first, second, raw_result))


def setup(bot):
    bot.add_cog(CustomCommands(bot))
