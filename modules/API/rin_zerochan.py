import json
import random

import discord
from discord.ext import commands
from rin_zerochan import zerochan

from ..utils.paginator import Pages
from ..utils import custom_exceptions


def return_search(search):
    searches = json.dumps(search)
    searches_json = json.loads(searches)
    return searches_json


def return_valid_image(search):
    images_list = return_search(search)
    random_image = images_list[random.randint(0, 23)]['thumb']
    if random_image:
        return random_image
    else:
        raise custom_exceptions.ResourceNotFound('Image not found.')


def return_unique_image(search):
    image_list = return_search(search)
    image = image_list['url']
    if image:
        return image
    else:
        raise custom_exceptions.ResourceNotFound('Image not found.')


def return_info(info):
    info = info[:1980] + '...' if len(info) >= 2000 else info
    return info


def return_tags(search):
    meta_list = return_search(search)
    meta = [i['name'] for i in meta_list]
    return meta


class ZeroChan:
    """Commands for ZeroChan integration"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['zc'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def zerochan(self, ctx, *, query: str):
        """Connects with the rin_zerochan library and retrieves images
        that matches you query."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            search = await zerochan.search(query)
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=return_valid_image(search))
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @zerochan.command(aliases=['img'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def image(self, ctx, image_id: str):
        """Input a image_id and output a entire image."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            search = await zerochan.image(image_id)
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=return_unique_image(search))
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @zerochan.command(aliases=['info'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def information(self, ctx, *, query: str):
        """Sends information about a tag."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            info = await zerochan.info(query)
            info = return_info(info)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send('```fix\n' + info + '\n```')
            await ctx.send(f'See more at: ```fix\nhttps://rin-zerochan.py.net/{query}\n```')
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @zerochan.command(aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meta(self, ctx, *, query: str):
        """Retrieve tags from meta-tags."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            search = await zerochan.meta(query)
            meta = return_tags(search)
            pages = Pages(ctx, lines=tuple(meta))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)


def setup(bot):
    bot.add_cog(ZeroChan(bot))
