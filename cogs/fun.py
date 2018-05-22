import random
import discord
import json
import os
from io import BytesIO
from collections import Counter
from discord.ext import commands
from utils import lists, permissions, http, default
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import urllib.request


class Fun_Commands:
    def __init__(self, bot):
        self.bot = bot
        self.counter = Counter()
        self.config = default.get("config.json")

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        return r[endpoint]

    @commands.command(name='nya')
    async def neko_search(self, ctx):
        """Posts a neko"""
        pic = await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/neko', 'url')
        await ctx.send(pic)
        
    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        pic = await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')
        await ctx.send(pic)
        
    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """
        arf = await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')
        await ctx.send(arf)
        
    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        quack = await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')
        await ctx.send(quack) 
        
    @commands.command(aliases=['fur'])
    async def floof(self, ctx):
        """Posts a cute floof :3""" 
        img = await self.randomimageapi(ctx, 'https://e926.net/post/show.json?limit=1&tags=cute%20solo', 'file_url')
        pic = random.choice(lists.floof)
        floof = discord.Embed(description=f"**{ctx.author.name}, heres a floof >w>**", color=discord.Color.blue())
        floof.set_image(url=img)
        try:
            await ctx.send(embed=floof)
        except:
            await ctx.send("aww i can't send embeds ;w;")

    @commands.command()
    @commands.is_nsfw() # TODO: Make a nsfw cog.
    async def yiff(self, ctx):
        """posts a yiff >:3 [thanks waspy]"""
        r = await self.randomimageapi(ctx, 'https://sheri.fun/api/v1/yiff', 'url')

        yiff = discord.Embed(title=">w>", color=0xDEADBF)
        yiff.set_image(url=r)

        try:
            await ctx.send(embed=yiff)
            self.bot.counter["yiff_viewed"] += 1
            
        except:
            await ctx.send("aww i can't send embeds ;w;")

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: str):
        """ Find the 'best' definition to your words """
        if not permissions.can_embed(ctx):
            return await ctx.send("I cannot send embeds here ;-;")

        url = await http.get(f'http://api.urbandictionary.com/v0/define?term={search}', res_method="json")

        if url is None:
            return await ctx.send("I think the API broke...")

        count = len(url['list'])
        if count == 0:
            return await ctx.send("Couldn't find your search in the dictionary...")
        result = url['list'][random.randint(0, count - 1)]

        definition = result['definition']
        if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

        embed = discord.Embed(colour=0xC29FAF, description=f"**{result['word']}**\n*by: {result['author']}*")
        embed.add_field(name='Definition', value=definition, inline=False)
        embed.add_field(name='Example', value=result['example'], inline=False)
        embed.set_footer(text=f"👍 {result['thumbs_up']} | 👎 {result['thumbs_down']}")

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I found something, but have no access to post it... [Embed permissions]")

    @commands.command()
    @commands.guild_only()
    async def say(self, ctx, *, text: str):
        """Makes me repeat something you say"""
        author = ctx.message.author
        guild = ctx.message.guild
        info = discord.Embed(title=f"{guild.name} ({guild.id})", description=f"**{author}**: {text}", color=discord.Color.dark_purple())
        text = text.replace("@everyone", "&everyone").replace("@here", "&here")
        try:
            await ctx.message.delete()
            await ctx.send(text)
            print(f"{author} said: {text}")
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
                await webhook.send(embed=info)
        except discord.Forbidden:
            await ctx.send("Am i allowed to manage messages?")

    @commands.command(aliases=['👏'])
    @commands.guild_only()
    async def clap(self, ctx, *, text_to_clap: str):
        """👏bottom👏text👏"""
        author = ctx.message.author
        guild = ctx.message.guild
        clapped_text = text_to_clap.replace("@everyone", "👏everyone").replace("@here", "👏here").replace(" ", "👏")
        clapped_text = f"👏{clapped_text}👏"
        info = discord.Embed(title=f"{guild.name} ({guild.id})", description=f"**{author}**: {text_to_clap}", color=discord.Color.gold())
        try:
            await ctx.message.delete()
            await ctx.send(clapped_text)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
                await webhook.send(embed=info)
        except discord.Forbidden:
            await ctx.send(clapped_text)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
                await webhook.send(content="no delet", embed=info)

    @commands.command(aliases=['randowo', 'owogen'])
    async def rowo(self, ctx):
        """Sends a random owo face"""
        owo = random.choice(lists.owos)
        await ctx.send(f"{owo} whats this?")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(aliases=['owolang'])
    async def hewwo(self, ctx, *, text: str):
        """Takes something you say and puts it in owo"""         
        owo_t = text.replace("n", "ny").replace("l", "w").replace("r", "w") #i was gonna add an @everyone and @here blocker but the r to w change already handles that XD
        await ctx.send(f"OwO {owo_t}")
        
    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        numbers = random.randint(0, 100)
        decimals = random.randint(0, 9)

        if numbers == 100:
            decimals = 0

        await ctx.send(f"I'd rate {thing} a **{numbers}.{decimals} / 100**")

    @commands.command(aliases=['noticemesenpai'])
    async def noticeme(self, ctx):
        """ Notice me senpai! owo """
        if not permissions.can_upload(ctx):
            return await ctx.send("I cannot send images here ;-;")

        bio = BytesIO(await http.get("https://i.alexflipnote.xyz/500ce4.gif", res_method="read"))
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        if (a == b == c):
            message = 'and won! 🎉'
        elif (a == b) or (a == c) or (b == c):
            message = 'and almost won (2/3)'
        else:
            message = 'and lost...'

        result = f"**{ctx.author.name}** rolled the slots...\n**[ {a} {b} {c} ]**\n{message}"
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Fun_Commands(bot))
