import discord
from utils import default, repo, http

class welcomersupport:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")


    async def on_message(self, msg):
        auto-help = self.bot.get_channel(454308883964362763)
        if ctx.channel != auto-help:
            pass
        else:
            if message.content.startswith('help'):
                help = discord.embed(title="Welcomer Support", description="`1.` How do i setup welcomer?\n"
                                                                           "`2.` How do i enable/disable images and text?\n"
                                                                           "`3.` How do i change image text?\n"
                                                                           "`5.` How do i choose a welcoming channel?\n"
                                                                           "`6.` How do i mention someone in the welcome message?")
                                                                           
