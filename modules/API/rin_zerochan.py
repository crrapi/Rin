import json
import traceback
from random import randint

from discord import Colour, Embed
from discord.ext import commands

from ..utils import custom_exceptions
from ..utils.paginator import Pages
from ..utils import zerochan


class ZeroChan:
    """Commands for ZeroChan integration"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['zc'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def zerochan(self, ctx, *, query: str, page=randint(0, 11)):
        """Connects with the rin-zerochan API and retrieves images
        that matches you query."""
        exceptions = (ValueError, Exception)
        try:
            search_str = await zerochan._search(query, page)
            search_list = json.dumps(search_str)
            images_list = json.loads(search_list)
            random_image = images_list[randint(0, 11)]['thumb']
            embed = Embed(color=Colour.red())
            embed.set_image(url=random_image)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.send(e)

    @zerochan.command(aliases=['img'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def image(self, ctx, id: str):
         """Input a image_id and output a entire image."""
         exceptions = (ValueError, Exception)
         try:
            search_str = await zerochan._image(id)
            search_list = json.dumps(search_str)
            image_list = json.loads(search_list)
            random_image = image_list['url']
            embed = Embed(color=Colour.red())
            embed.set_image(url=random_image)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
         except exceptions as e:
             await ctx.send(e)

    @zerochan.command(aliases=['info'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def information(self, ctx, *, query: str):
        """Sends information about a tag."""
        exceptions = (ValueError, Exception)
        try:
            info = await zerochan._info(query)
            info = info[:1980] + '...' if len(info) >= 2000 else info
            await ctx.send('```fix\n' + info + '\n```')
            await ctx.send(f'See more at: ```fix\nhttps://zerochan.net/{query}\n```')
        except exceptions as e:
            await ctx.send(e)

    @zerochan.command(aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def meta(self, ctx, *, query: str, page=randint(0, 11)):
        """Retrieve tags from meta-tags."""
        exceptions = (ValueError, Exception)
        try:
            search_str = await zerochan._meta(query, page)
            search_list = json.dumps(search_str)
            meta_list = json.loads(search_list)
            meta = [i['name'] for i in meta_list]
            pages = Pages(ctx, lines=tuple(meta))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except exceptions as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(ZeroChan(bot))
