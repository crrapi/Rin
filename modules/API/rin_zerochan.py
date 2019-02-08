from random import choice, randint

from aiohttp import ClientSession
from discord import Colour, Embed
from discord.ext import commands

from ..utils import custom_exceptions
from ..utils.paginator import Pages


class ZeroChan:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['zc'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def zerochan(self, ctx, *, query: str, pages=randint(1, 11)):
        """Connects with the rin-zerochan API and retrieves images
        that matches you query."""
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/search/{query}/{pages}') as response:
                exceptions = (custom_exceptions.ResourceNotFound, custom_exceptions.Error)
                try:
                    data = (await response.json())['data']
                    random_image = choice(data)['thumb']
                    if not random_image:
                        raise custom_exceptions.ResourceNotFound('Image not found.')
                    embed = Embed(color=Colour.red())
                    embed.set_image(url=random_image)
                    await ctx.message.add_reaction('\U00002705')
                    await ctx.send(embed=embed)
                except exceptions as e:
                    await ctx.send(e)

    @zerochan.command(aliases=['i'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def image(self, ctx, id: str):
        """Input a image_id and output a entire image."""
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/image/{id}') as response:
                exceptions = (custom_exceptions.ResourceNotFound, custom_exceptions.Error)
                try:
                    data = (await response.json())['data']
                    image = data['url']
                    if not image:
                        raise custom_exceptions.ResourceNotFound('Image not found.')
                    embed = Embed(color=Colour.red())
                    embed.set_image(url=image)
                    await ctx.message.add_reaction('\U00002705')
                    await ctx.send(embed=embed)
                except exceptions as e:
                    await ctx.send(e)

    @zerochan.command(aliases=['info', 'in'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def information(self, ctx, *, query: str):
        """Sends information about a tag."""
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/info/{query}') as response:
                exceptions = (custom_exceptions.ResourceNotFound, custom_exceptions.Error)
                try:
                    info = (await response.json())['data']
                    if not info:
                        raise custom_exceptions.ResourceNotFound('Info not found.')
                    info = info[:1980] + '...' if len(info) >= 2000 else info
                    await ctx.send('```fix\n' + info + '\n```')
                    await ctx.send(f'See more at: ```fix\nhttps://zerochan.net/{query}\n```')
                except exceptions as e:
                    await ctx.send(e)

    @zerochan.command(aliases=['m'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def meta(self, ctx, *, query: str):
        """Retrieve tags from meta-tags."""
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/meta/{query}') as response:
                exceptions = (custom_exceptions.ResourceNotFound, custom_exceptions.Error)
                try:
                    data = (await response.json())['data']
                    if not data:
                        raise custom_exceptions.ResourceNotFound('Tags not found')
                    pages = Pages(ctx, lines=tuple(i['name'] for i in data))
                    await ctx.message.add_reaction('\U00002705')
                    await pages.paginate()
                except exceptions as e:
                    await ctx.send(e)


def setup(bot):
    bot.add_cog(ZeroChan(bot))
