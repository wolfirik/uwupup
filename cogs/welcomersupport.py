import discord
from utils import default, repo, http
import random

class welcomersupport:
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")


    async def on_message(self, msg):
        helpchan = self.bot.get_channel(443444305051254787)
        if msg.channel.id != 443444305051254787:
            return
        elif msg.author.bot:
            return
        else:
            if "help" in msg.content:
                bd = ":small_blue_diamond:"
                welcomer = self.bot.get_user(330416853971107840)
                help = discord.Embed(title="Welcomer Support", description=f"{bd} `1.` How do i setup welcomer?\n"
                                                                           f"{bd} `2.` How do i enable/disable images and text?\n"
                                                                           f"{bd} `3.` How do i change image text?\n"
                                                                           f"{bd} `5.` How do i choose a welcoming channel?\n"
                                                                           f"{bd} `6.` How do i mention someone in the welcome message?\n"
                                                                           f"{bd} `7.` How do i change the background?\n"
                                                                           f"{bd} `8.` How do i get the markdown?\n"
                                                                           f"{bd} `9.` How do i set a custom image?\n"
                                                                           f"{bd} `10.` How do i use gif backgrounds?\n"
                                                                           f"{bd} `11.` How do i change the welcome colours?\n"
                                                                           f"{bd} `12.` How do i change the prefix?\n"
                                                                           f"{bd} `13.` My question isn't here\n"
                                                                           "*send the number coressponding to your issue to get help*", color=discord.Color.blue())
                help.set_footer(text="Thank You for choosing welcomer!", icon_url=welcomer.icon_url)
                await helpchan.send(content=f"{ctx.author.mention}", embed=help)
            else:
                pass

def setup(bot):
    bot.add_cog(welcomersupport(bot))
