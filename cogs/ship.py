import discord
from random import randint
import random
from discord.ext import commands

class Ship:
    """hai"""

    def __init__(self, bot):
        self.bot = bot
        self.color = 0x254d16


    @commands.command()
    @commands.guild_only()
    async def ship(self, ctx, user : discord.Member, *, user2 : discord.Member=None):
        """Checks the shiprate for 2 users"""
        author = ctx.message.author
        owo = self.bot.get_user(365255872181567489)
        skull = self.bot.get_user(158750488563679232)
        draggy = self.bot.get_user(254599284425621505)
        heh = self.bot.get_user(185938944460980224)
        if not user2:
            user2 = author
        # preset ships don't mind these...
        if not user:
            await ctx.send("can't ship nothing y'know..")
        elif user.id == user2.id:
            await ctx.send("i-i can't ship the same person..")
        elif user.id == author.id and user2.id == author.id:
            await ctx.send(f"wow, you're in love with yourself, huh {ctx.author.name}?")
        # ships with owopup
        elif user == owo and user2 == author or user2 == owo and user == author:
            blushes = ["m-me..? 0////0", "m-me..? >////<"]
            return await ctx.send(random.choice(blushes))
        elif user == draggy and user2 == skull or user2 == draggy and user == skull:
            ship = discord.Embed(title=" " + user.display_name + "  x  " + user2.display_name + " ", description="**69%** **`██████████`** ❤", colour=0xDEADBF)
            return await ctx.send(embed=ship)
        elif user2 == heh and user == skull or user == skull and user2 == heh:
            ship = discord.Embed(title=" " + user.display_name + " x " + user2.display_name + " ", description="**100%** **`██████████`** 💞", colour=self.color)
            return await ctx.send(embed=ship)

        else:
            n = randint(1, 100)
            if n > 50:
                 emoji = '❤'
            else:
                emoji = '💔'
            if n == 100:
                bar = "██████████"
                emoji = '💞'
            elif n > 90:
                bar = "█████████."
                emoji = '💕'
            elif n > 80:
                bar = "████████.."
                emoji = '😍'
            elif n > 70:
                bar = "███████..."
                emoji = '💗'
            elif n > 60:
                bar = "██████...."

            elif n > 50:
                bar = '█████.....'
                emoji = '❤'
            elif n > 40:
                bar = "████......"
                emoji = '💔'
            elif n > 30:
                bar = "███......."
                emoji = '💔'
            elif n > 20:
                bar = "██........"
                emoji = '💔'
            elif n > 10:
                bar = "█........."
                emoji = '💔'
            elif n < 10:
                bar = ".........."
                emoji ='🖤'
            else:
                bar = ".........."
                emoji ='🖤'

            link = "https://cdn.discordapp.com/emojis/359420199050674176.png" # never used this :P
            ship = discord.Embed(title=" " + user.display_name + "  x  " + user2.display_name + " ", description="**{}%** **`{}`** {}".format(n, bar, emoji), color=self.color)
            await ctx.send(embed=ship)
            # < the invisible character if needed.

    #@commands.command()
    #@commands.guild_only()
    #async def shipname(self, ctx, user : discord.Member=None, user2 : discord.Member=None):
        #"""Generates a shipname for two users owo"""
        #author = ctx.message.author
        #if not user2:
            #user2 = author

        #elif not user:
            #await ctx.send("ack, i need people y'know :P")

        #elif user.id == user2.id:
            #await ctx.send("{} >:1".format(user.name))
        #else:

            #await ctx.send("")

def setup(bot):
    bot.add_cog(Ship(bot))
