import discord
from discord.ext import commands, formatter

class Help:
    """OwOpup's help formatter"""

    def __init__(self, bot):
        self.bot = bot

async def send_help_dm(ctx):
    _help = await ctx.bot.formatter.format_help_for(ctx, ctx.bot)

    for page in _help:
        page = page.replace("```", "`") # URGENT TODO: Stop being lazy and write a custom help command.
        page = discord.Embed(title="owopup", description=page, color=0x254d16)
        await ctx.author.send(embed=page)

async def send_help(ctx):
    _help = await ctx.bot.formatter.format_help_for(ctx, ctx.bot)

    for page in _help:
        page = page.replace("```", "`") 
        page = discord.Embed(title="owopup", description=page, color=0x254d16)
        page.set_footer(text="You most likely had dms blocked for me so i sent it here.")
        await ctx.send(embed=page)

    @commands.command()
    async def help(self, ctx):
        """This does stuff!"""
        try: 
            await ctx.send(f"oki, {ctx.author.name} check your dms uwu")
            await send_help_dm(ctx)
        except:
            await send_help(ctx)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
