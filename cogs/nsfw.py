# Credit for this cog: https://github.com/robingall2910/RobTheBoat
import random
import json
import urllib.request

from discord.ext import commands
from utils import permissions


# This is the limit to how many posts are selected
limit = 50

class NSFW():
    def __init__(self, bot):
        self.bot = bot

    @checks.is_nsfw_channel()
    @commands.command()
    async def rule34(self, ctx, *, tags:str):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        try:
            data = json.loads(requests.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, tags)).text)
        except json.JSONDecodeError:
            await ctx.send("No results found for `{}`".format(tags))
            return

        count = len(data)
        if count == 0:
            await ctx.send("No results found for `{}`".format(tags))
            return
        image_count = 4
        if count < 4:
            image_count = count
        images = []
        for i in range(image_count):
            image = data[random.randint(0, count)]
            images.append("http://img.rule34.xxx/images/{}/{}".format(image["directory"], image["image"]))
        await ctx.send("Showing {} out of {} results for `{}`\n{}".format(image_count, count, tags, "\n".join(images)))

    @checks.is_nsfw_channel()
    @commands.command()
    async def e621(self, ctx, *, t:str):
        """Searches e621.net for the specified tagged images"""
        #needed for searching
        header = {'Content-Type': 'application/json', 'User-Agent': 'owopup by skullbite'}
        #for json
        tags = t.replace(" ", "%20")
        #for human readable tags
        url = "https://e621.net/post/index.json?limit={}&tags={}".format(limit, tags)
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        try:
            p = urllib.request.Request(url, None, header)
            q = urllib.request.urlopen(p).read()
            data = json.loads(q.decode())
            #data = json.loads(str(requests.get(url, headers=header)))
        except json.JSONDecodeError:
            await ctx.send("JSON Decode Error! Please report this with .notifydev.")
            print("e621 json decode error")
            return
        except IndexError:
            await ctx.send("Nothing was found with `{}`. Either see if your tags are correctly spelt, or adjust it.".format(t))
        count = len(data)
        if count == 0:
            await ctx.send("Nothing was found with `{}`. Either see if your tags are correctly spelt, or adjust it.".format(t ))
            return
        image_count = 4
        if count < 4:
            image_count = count
        images = []
        for i in range(image_count):
            images.append(data[random.randint(0, count)]["file_url"])
        await ctx.send("Showing `{}` out of `{}` results for `{}`\n{}".format(image_count, count, t, "\n".join(images)))

    @checks.is_nsfw_channel()
    @commands.command()
    async def yandere(self, ctx, *, tags:str):
        """Searches yande.re for the specified tagged images"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        try:
            data = json.loads(requests.get("https://yande.re/post/index.json?limit={}&tags={}".format(limit, tags)).text)
        except json.JSONDecodeError:
            await ctx.send("No results found for `{}`".format(tags))
            return
        count = len(data)
        if count == 0:
            await ctx.send("No results found for `{}`".format(tags))
            return
        image_count = 4
        if count < 4:
            image_count = count
        images = []
        for i in range(image_count):
            images.append(data[random.randint(0, count)]["file_url"])
        await ctx.send("Showing {} out of {} results for `{}`\n{}".format(image_count, count, tags, "\n".join(images)))

    @checks.is_nsfw_channel()
    @commands.command()
    async def danbooru(self, ctx, *, tags:str):
        """Searches danbooru.donmai.us for the specified tagged images"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        try:
            data = json.loads(requests.get("https://danbooru.donmai.us/post/index.json?limit={}&tags={}".format(limit, tags)).text)
        except json.JSONDecodeError:
            await ctx.send("No results found for `{}`".format(tags))
            return
        count = len(data)
        if count == 0:
            await ctx.send("No results found for `{}`".format(tags))
            return
        image_count = 4
        if count < 4:
            image_count = count
        images = []
        for i in range(image_count):
            try:
                images.append("http://danbooru.donmai.us{}".format(data[random.randint(0, count)]["file_url"]))
            except KeyError:
                await ctx.send(data["message"])
                return
        await ctx.send("Showing {} out of {} results for `{}`\n{}".format(image_count, count, tags, "\n".join(images)))

    @checks.is_nsfw_channel()
    @commands.command()
    async def gelbooru(self, ctx, *, tags:str):
        """Searches gelbooru.com for the specified tagged images"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        try:
            data = json.loads(requests.get("https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, tags)).text)
        except json.JSONDecodeError:
            await ctx.send("No results found for `{}`".format(tags))
            return
        count = len(data)
        if count == 0:
            await ctx.send("No results found for `{}`".format(tags))
            return
        image_count = 4
        if count < 4:
            image_count = count
        images = []
        for i in range(image_count):
            try:
                images.append("http:{}".format(data[random.randint(0, count)]["file_url"]))
            except KeyError:
                await ctx.send(data["message"])
                return
        await ctx.send("Showing {} out of {} results for `{}`\n{}".format(image_count, count, tags, "\n".join(images)))

    @checks.is_nsfw_channel()
    @commands.command()
    async def xbooru(self, ctx, *, tags: str):
        """Searches xbooru.com for the specified tagged images"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.channel.trigger_typing()
        try:
            data = json.loads(requests.get("https://xbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, tags)).text)
        except json.JSONDecodeError:
            await ctx.send("No results found for `{}`".format(tags))
            return
        count = len(data)
        if count == 0:
            await ctx.send("No results found for `{}`".format(tags))
            return
        image_count = 4
        if count < 4:
            image_count = count
        images = []
        for i in range(image_count):
            try:
                post = data[random.randint(0, count)]
                images.append("http://img3.xbooru.com/images/{}/{}".format(post["directory"], post["image"]))
            except KeyError:
                await ctx.send(data["message"])
                return
        await ctx.send("Showing {} out of {} results for `{}`\n{}".format(image_count, count, tags, "\n".join(images)))

def setup(bot):
    bot.add_cog(NSFW(bot))
