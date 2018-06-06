import discord
from discord.ext import commands
from data import Bot


bot = Bot(command_prefix=commands.when_mentioned_or("uwu "), prefix=commands.when_mentioned_or("uwu "), pm_help=True)

@bot.event
async def on_message_delete(message):
    author = ctx.author
    chan = bot.get_channel(453991541434744832)
    await chan.send("Message from {author} deleted\n```{message}```")
