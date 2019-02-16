import json
import random

import discord
from discord.ext import commands
from rin_zerochan import zerochan

from ..utils.paginator import Pages
from ..utils import custom_exceptions


class ZeroChan:
    """Commands for ZeroChan integration"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['zc'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def zerochan(self, ctx, *, query: str, page=random.randint(1, 10)):
        """Connects with the rin_zerochan library and retrieves images
        that matches you query."""
        exceptions = (ValueError, Exception)
        try:
            search_str = await zerochan.search(query, page)
            search_list = json.dumps(search_str)
            images_list = json.loads(search_list)
            random_image = random.choice(images_list)['thumb']
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=random_image)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @zerochan.command(aliases=['img'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def image(self, ctx, image_id: str):
        """Input a image_id and output a entire image."""
        exceptions = (custom_exceptions.ResourceNotFound, ValueError, Exception)
        try:
            search_str = await zerochan.image(image_id)
            search_list = json.dumps(search_str)
            image_list = json.loads(search_list)
            random_image = image_list['url']
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=random_image)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @zerochan.command(aliases=['info'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def information(self, ctx, *, query: str):
        """Sends information about a tag."""
        exceptions = (ValueError, Exception)
        try:
            info = await zerochan.info(query)
            info = info[:1980] + '...' if len(info) >= 2000 else info
            await ctx.send('```fix\n' + info + '\n```')
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(f'See more at: ```fix\nhttps://rin-zerochan.py.net/{query}\n```')
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @zerochan.command(aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meta(self, ctx, *, query: str, page=random.randint(1, 10)):
        """Retrieve tags from meta-tags."""
        exceptions = (ValueError, Exception)
        try:
            search_str = await zerochan.meta(query, page)
            search_list = json.dumps(search_str)
            meta_list = json.loads(search_list)
            meta = [i['name'] for i in meta_list]
            pages = Pages(ctx, lines=tuple(meta))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)


def setup(bot):
    bot.add_cog(ZeroChan(bot))
