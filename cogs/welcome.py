import discord
from discord.ext import commands
from utils import DataIO as dataIO
import os
import asyncio
from random import choice as rand
from copy import deepcopy

# interpreting from irdumbs welcome cog

de_greeting = "hai {0.mention}! Welcome to {1.name}!"
de_settings = {"MSGS": [de_greeting], "ON": False, "CHANNEL": None}
path = "data/welcome/settings.json"

class Welcome:
    """Cog for welcoming new users to the server"""   
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(path)

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_server=True)
    async def welcomeset(self, ctx):
        """Sets welcome module settings"""
        if guild.id not in self.settings:
            self.settings[guild.id] = deepcopy(de_settings)
            self.settings[guild.id]["CHANNEL"] = None
            dataIO.save_json(path, self.settings)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            msg = "```"
            msg += "Random GREETING: {}\n".format(rand(self.settings[guild.id]["MSGS"].format(author, guild)))
            msg += "CHANNEL: #{}\n".format(self.get_welcome_channel(guild))
            msg += "ON: {}\n".format(self.settings[guild.id]["ON"])
            msg += "```"
            await ctx.send(msg)

    @welcomeset.command()
    async def test(self, ctx):
        """oof"""
        await ctx.send("hecc.")

    def get_welcome_channel(self, guild):
        try:
            return guild.get_channel(self.settings[guild.id]["CHANNEL"])
        except:
            return None

    async def member_join(guild):
        guild = member.guild
        if guild.id not in self.settings:
            self.settings[guild.id] = deepcopy(de_settings)
            self.settings[guild.id]["CHANNEL"] = None
            dataIO.save_json(settings_path, self.settings)
        if not self.settings[guild.id]["ON"]:
            return
        if guild is None:
            print("Guild is None. Private Message or some new fangled "
                  "Discord thing?.. Anyways there be an error, "
                  "the user was {}".format(member.name))
            return

        msg = rand(self.settings[guild.id]["MSGS"])

        # grab the welcome channel
        channel = self.get_welcome_channel(guild)
        if channel is None:  # complain even if only whisper
            print('welcome.py: Channel not found. It was most '
                  'likely deleted. User joined: {}'.format(member.name))
            return
        # finally, welcome them
        await channel.send(msg.format(member, guild))

def check_folders():
    if not os.path.exists("data/welcome"):
        print("Creating data/welcome folder...")
        os.makedirs("data/welcome")


def check_files():
    f = path
    if not dataIO.is_valid_json("data/welcome/settings.json"):
        print("Creating welcome settings.json...")
        dataIO.save_json(f, {})
    else:  # consistency check
        current = dataIO.load_json(f)
        for k, v in current.items():
            if v.keys() != de_settings.keys():
                for key in de_settings.keys():
                    if key not in v.keys():
                        current[k][key] = deepcopy(de_settings)[key]
                        print("Adding " + str(key) +
                              " field to welcome settings.json")
        # upgrade. Before GREETING was 1 string
        for guild in current.values():
            if isinstance(guild["MSGS"], str):
                guild["MSGS"] = [guild["MSGS"]]
        dataIO.save_json(f, current)


def setup(bot):
    check_folders()
    check_files()
    n = Welcome(bot)
    bot.add_listener(n.member_join, "on_member_join")
    bot.add_cog(n)
