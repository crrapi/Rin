import random

import discord
from discord.ext import commands
from rin_zerochan import zerochan

from ..utils import custom_exceptions
from ..utils.paginator import Pages


def return_valid_image(search):
    images_list = search
    random_image = random.choice(images_list)['thumb']
    if not random_image:
        raise custom_exceptions.ResourceNotFound('Image not found.')
    return random_image


def return_unique_image(search):
    image_list = search
    image = image_list['url']
    if not image:
        raise custom_exceptions.ResourceNotFound('Image not found.')
    return image


def return_info(info):
    if not info:
        raise custom_exceptions.ResourceNotFound('Info not found.')
    info = info[:1980] + '...' if len(info) >= 2000 else info
    return info


def return_tags(search):
    meta_list = search
    meta = [i['name'] for i in meta_list]
    if not meta:
        raise custom_exceptions.ResourceNotFound('Meta not found. ')
    return meta


class ZeroChan(commands.Cog):
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
            search = await zerochan.search(query, random.randint(1, 100))
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=return_valid_image(search))
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e, delete_after=5)

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
            await ctx.send(e, delete_after=10)

    @zerochan.command(aliases=['info'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def information(self, ctx, *, query: str):
        """Sends information about a tag."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            info = await zerochan.info(query)
            info = return_info(info)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send('```\n' + info + '\n```')
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e, delete_after=10)

    @zerochan.command(aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meta(self, ctx, *, query: str):
        """Retrieve tags from meta-tags."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            search = await zerochan.meta(query, 1)
            meta = return_tags(search)
            pages = Pages(ctx, lines=tuple(meta))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e, delete_after=10)


def setup(bot):
    bot.add_cog(ZeroChan(bot))
