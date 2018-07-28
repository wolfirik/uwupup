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
import requests

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
        meow = discord.Embed(description=f"n-nya!!", color=0xcb27ff)
        meow.set_image(url=pic)
        await ctx.send(embed=meow)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        """ Posts a random cat """
        pic = await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')
        meow = discord.Embed(description=f"m-meow. hmph", color=0x002d55)
        meow.set_image(url=pic)
        await ctx.send(embed=meow)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        """ Posts a random dog """
        arf = await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')
        if arf.endswith(".mp4"):
            await ctx.send(arf)
        else:
            embed = discord.Embed(title="arf arf", color=0x36393e).set_image(url=arf)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        quack = await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')
        await ctx.send(quack)

    @commands.command(aliases=['fur'])
    async def floof(self, ctx):
        """Posts a cute floof :3"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ksoft.si/meme/random-image', params={
                    "tag": "floofs"
                }, headers={"Authorization": "Token b46b0c17c5ad53fff384f625cabd390d16e64c47"}) as resp:
                    data = await resp.json()
        except:
            return await ctx.send("I think the api is being dumb.. try again later..")
        floof = discord.Embed(description=f"**{ctx.author.name}, heres a floof :feet:**", color=0xf44444)
        floof.set_image(url=data["url"])
        try:
            await ctx.send(embed=floof)
        except:
            await ctx.send("aww i can't send embeds ;w;")

    @commands.command()
    async def blush(self, ctx):
        """0///0"""
        try:
            async with aiohttp.ClientSession(headers={'User-Agent': 'Chrome/60.0.3112.113'}) as session:
                async with session.get(f'https://e926.net/post/index.json?limit=1&tags=order:random%20blush%20-equine%20fur%20solo') as get:
                    resp = await get.json()
                    floof = discord.Embed(description=f"**{ctx.author.name}, you're bl-blushing..! 0////0**", color=0xf44444)
                    floof.set_image(url=resp['file_url'])
                    await ctx.send(embed=floof)
        except Exception as e:
            return await ctx.send(e)
        try:
            pass
        except:
            await ctx.send("aww i can't send embeds ;w;")
            

    @commands.command(aliases=['hugge'])
    @commands.guild_only()
    async def hug(self, ctx, user: discord.Member=None):
        """Give someone a hug >w<"""
        if not user:
            await ctx.send("u-uhm who do you wanna hug..?")
        elif user == self.bot.user:
            await ctx.send("d-don't hug me..!")
        elif user == ctx.author:
            await ctx.send(f"maybe someone other than your self {ctx.author.name}..?")

        else:
            try:
                r = requests.get("https://sheri.fun/api/v1/img/hug", headers={"key": os.environ["MURR"]}).json().get("url")
                hugge = discord.Embed(description=f"**{ctx.author.name} gave {user.name} a hug uwu**", color=0xd25e92)
                hugge.set_image(url=r)
                await ctx.send(embed=hugge)
            except Exception as e:
                return await ctx.send(e)
            try:
                pass
            except discord.Forbidden:
                await ctx.send("aww i can't send embeds.. ;w;")
            except:
                await ctx.send("something oofed..")

    @commands.command()
    @commands.guild_only()
    async def pat(self, ctx, user: discord.Member=None):
        """pat pat :3 (not that may pats right now)"""
        if not user:
            await ctx.send("who do you wanna pat..?")
        elif user == self.bot.user:
            await ctx.send("i-i'm good on pats for now but thanks.. uwu")
        elif user == ctx.author:
            await ctx.send(f"maybe someone other than your self {ctx.author.name}..?")

        else:
            try:
                async with aiohttp.ClientSession(headers={'User-Agent': 'Chrome/60.0.3112.113'}) as session:
                    async with session.get(f'http://e926.net/post/index.json?tags=head_pat%20-young%20order:random&limit=1') as get:
                        resp = await get.json()
                        pat = discord.Embed(description=f"**{ctx.author.name} pat {user.name} on the head for being good..**", color=0x6a1b9a)
                        pat.set_image(url=resp['file_url'])
                        await ctx.send(embed=pat)
            except:
                return await ctx.send("I think e926 is being dumb.. try again later..")
            try:
                pass
            except discord.Forbidden:
                await ctx.send("aww i can't send embeds.. ;w;")
            except:
                await ctx.send("something oofed..")

    @commands.command(aliases=['snuggle'])
    @commands.guild_only()
    async def cuddle(self, ctx, user: discord.Member=None):
        """cuddle a cutie uwu"""
        if not user:
            await ctx.send("u-uhm who do you wanna cuddle..? owo")
        elif user == self.bot.user:
            await ctx.send("d-don't cuddle me..!")
        elif user == ctx.author:
            await ctx.send(f"maybe someone other than your self {ctx.author.name}..?")
        else:
            try:
                r = requests.get("https://sheri.fun/api/v1/img/cuddles", headers={"key": os.environ["MURR"]}).json().get("url")
                cuddle = discord.Embed(description=f"**{ctx.author.name} gave {user.name} a nice long \"hug\" OwO**", color=0x3f51b5)
                cuddle.set_image(url=r)
                await ctx.send(embed=cuddle)
            except:
                return await ctx.send("I think e926 is being dumb.. try again later..")
            try:
                pass
            except discord.Forbidden:
                await ctx.send("aww i can't send embeds.. ;w;")
            except:
                await ctx.send("something oofed..")

    @commands.command()
    @commands.guild_only()
    async def lick(self, ctx, user: discord.Member=None):
        """lick someone >w<"""
        if not user:
            await ctx.send("u-uhm who do you wanna lick..?")
        elif user == self.bot.user:
            await ctx.send("d-don't lick me..! >~<")
        elif user == ctx.author:
            await ctx.send(f"maybe someone other than your self {ctx.author.name}..?")
        else:
            try:
                async with aiohttp.ClientSession(headers={'User-Agent': 'Chrome/60.0.3112.113'}) as session:
                    async with session.get(f'https://e926.net/post/index.json?limit=1&tags=-kiss%20order:random%20face_lick%20-equine%20-belly_expansion') as get:
                        resp = await get.json()
                        r = requests.get("https://sheri.fun/api/v1/img/lick", headers={"key": os.environ["MURR"]}).json().get("url")
                        lick = discord.Embed(description=f"**{ctx.author.name} decided to get {user.name}'s fur wet ~w~**", color=0x2e7d32)
                        lick.set_image(url=r)
                        await ctx.send(embed=lick)
            except:
                return await ctx.send("I think e926 is being dumb.. try again later..")
            try:
                pass
            except discord.Forbidden:
                await ctx.send("aww i can't send embeds.. ;w;")
            except:
                await ctx.send("something oofed..")

    @commands.command()
    @commands.guild_only()
    async def kiss(self, ctx, user: discord.Member=None):
        """give someone a kiss >w>"""
        eye = self.bot.get_emoji(451796122311327745)
        if not user:
            await ctx.send("u-uhm who do you wanna kiss..?")
        elif user == self.bot.user:
            await ctx.send("i-i don't want any k-kisses..!")
        elif user == ctx.author:
            await ctx.send(f"maybe someone other than your self {ctx.author.name}..?")
        else:
            try:
                async with aiohttp.ClientSession(headers={'User-Agent': 'Chrome/60.0.3112.113'}) as session:
                    async with session.get(f'https://e926.net/post/index.json?limit=1&tags=kiss%20cute%20fur%20-equine%20order:random') as get:
                        resp = await get.json()
                        r = requests.get("https://sheri.fun/api/v1/img/kiss", headers={"key": os.environ["MURR"]}).json().get("url")
                        kiss = discord.Embed(description=f"**{ctx.author.name} showed their feelings for {user.name} \❤w\❤**", color=0xe91e63)
                        kiss.set_image(url=r)
                        await ctx.send(embed=kiss)
            except:
                return await ctx.send("I think e926 is being dumb.. try again later..")
            try:
                pass
            except discord.Forbidden:
                await ctx.send("aww i can't send embeds.. ;w;")
            except:
                await ctx.send("something oofed..")

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: str):
        """ Find the 'best' definition to your words """
        if not ctx.channel.is_nsfw():
            return await ctx.send("Due to changes in the discord TOS, urban is a nsfw command now. Please use it in a nsfw channel.")
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
            await ctx.send(text)
            print(f"{author} said: {text}")
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(os.environ["WEBHOOK"], adapter=AsyncWebhookAdapter(session))
                await webhook.send(content="no delet mode", embed=info)

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
        owo_t = text.replace("n", "ny").replace("l", "w").replace("r", "w").replace("N", "NY").replace("L", "W").replace("R", "W") #i was gonna add an @everyone and @here blocker but the r to w change already handles that XD
        await ctx.send(owo_t)

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
                         
     #ignore this command
    @commands.command(aliases=['stacks', 'ss'], hidden=True)
    async def samurai(self, ctx):
        await ctx.send("Samurai sucks and is not a furry lol")
        await asyncio.sleep(3)
        await ctx.send("uwu fuck u samuwai")

def setup(bot):
    bot.add_cog(Fun_Commands(bot))
