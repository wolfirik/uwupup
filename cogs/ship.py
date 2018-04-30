import discord
from random import randint
from discord.ext import commands

class ship:
    """hai"""

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @commands.guild_only()
    async def ship(self, ctx, user : discord.Member, *, user2 : discord.Member=None):
        """Checks the shiprate for 2 users"""
        author = ctx.message.author
        
        if not user2:
            user2 = author
        # preset ships don't mind these...
        if user.id == user2.id:
            await ctx.send("i-i can't ship the same person..")
        # ships with owopup
        elif user.id == 365255872181567489 and user2.id == ctx.message.author or user2.id == 365255872181567489 and user.id == ctx.message.author:
            await ctx.send("0////0")
        elif user.id == 212726258188943360 and user2.id == 158750488563679232 or user2.id == 212726258188943360 and user.id == 15875048856367923:
            ship = discord.Embed(title=" " + user.display_name + "  x  " + user2.display_name + " ", description="**69%** **`██████████`** ❤", colour=0xDEADBF)
            await ctx.send(embed=ship)
        elif user2.id == 212726258188943360 and user.id == 158750488563679232 or user.id == 212726258188943360 and user2.id == 158750488563679232:
            ship = discord.Embed(title=" " + user.display_name + " x " + user2.display_name + " ", description="**100%** **`██████████`** 💞", colour=0xDEADBF)
            await ctx.send(embed=ship)

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
                bar = "█████████ "
                emoji = '💕'
            elif n > 80:
                bar = "████████  "
                emoji = '😍'
            elif n > 70:
                bar = "███████   "
                emoji = '💗'
            elif n > 60:
                bar = "██████    "
                
            elif n > 50:
                bar = '█████     '
                emoji = '❤'
            elif n > 40:
                bar = "████      "
                emoji = '💔'
            elif n > 30:
                bar = "███       "
                emoji = '💔'
            elif n > 20:
                bar = "██        "
                emoji = '💔'
            elif n > 10:
                bar = "█         "
                emoji = '💔'
            elif n < 10:
                bar = "          "
                emoji ='🖤'
            else:
                bar = "          "
                emoji ='🖤'

            link = "https://cdn.discordapp.com/emojis/359420199050674176.png"
            ship = discord.Embed(title=" " + user.display_name + "  x  " + user2.display_name + " ", description="**{}%** **`{}`** {}".format(n, bar, emoji), colour=0xDEADBF)
            await ctx.send(embed=ship)
            # < the invisible character if needed.

    @commands.command()
    @commands.guild_only()
    async def shipname(self, ctx, user : discord.Member=None, user2 : discord.Member=None):     
        """Generates a shipname for two users owo"""
        author = ctx.message.author
        if not user2:
            user2 = author
       
        if not user:
            await ctx.send("ack, i need people y'know :P")
        
        if user.id == user2.id:
            await ctx.send("{} >:1".format(user.name))
        else:
            await ctx.send("lemme work! \n- Skull")
    
def setup(bot):
    bot.add_cog(ship(bot))
