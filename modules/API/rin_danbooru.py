import random
import re

import discord
from discord.ext import commands
from pybooru import Danbooru as Client

from ..utils import custom_exceptions
from ..utils.paginator import Pages


def check_query(query):
    query = query.lower().split()
    if 'rating' in query:
        raise custom_exceptions.NSFWException('Good try, pervy!')
    if len(query) >= 2:
        raise custom_exceptions.Error('You can\'t input 2 or more tags.')
    query = ' '.join(query)
    return query


def return_tags(list_tags):
    related_tags = [i['related_tags'] for i in list_tags]
    if not related_tags:
        raise custom_exceptions.ResourceNotFound('Tags not found.')
    tags = re.sub(r'[0-9.]+', '', ''.join(related_tags)).split()
    return tags


def check_nsfw(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        pass
    elif ctx.channel.nsfw:
        pass
    else:
        raise custom_exceptions.NSFWException('NSFW commands only in NSFW channels')


def return_valid_image(post):
    file_url = post[0]['file_url']
    source = post[0]['source']
    if file_url:
        return file_url
    elif source:
        return source
    else:
        raise custom_exceptions.ResourceNotFound('Image not found.')


class Danbooru:
    """Commands for Danbooru integration"""

    def __init__(self, bot):
        self.bot = bot
        self.client = Client('danbooru')

    @commands.group(aliases=['db'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def danbooru(self, ctx, *, query: str):
        """Connects with the Danbooru client and retrieve a random image
        from a post list (only SFW channels)."""
        exceptions = (custom_exceptions.NSFWException, custom_exceptions.ResourceNotFound,
                      custom_exceptions.Error, Exception)
        try:
            query = check_query(query)
            post = self.client.post_list(tags='rating:safe ' + query, page=random.randint(1, 1000), limit=1)
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=return_valid_image(post))
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @danbooru.command(aliases=['n'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def nsfw(self, ctx, *, query: str):
        """Connects with Danbooru client and retrieve a random image
        from a post list (only NSFW channels)."""
        exceptions = (custom_exceptions.NSFWException, custom_exceptions.ResourceNotFound,
                      Exception)
        try:
            check_nsfw(ctx)
            query = check_query(query)
            post = self.client.post_list(tags=query, page=random.randint(1, 1000), limit=1)
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_image(url=return_valid_image(post))
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)

    @danbooru.command(aliases=['t'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def tags(self, ctx, *, query: str):
        """Retrieves tags that matches you query."""
        exceptions = (custom_exceptions.ResourceNotFound, Exception)
        try:
            list_tags = self.client.tag_list(name_matches=query)
            tags = return_tags(list_tags)
            pages = Pages(ctx, lines=tags)
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except exceptions as e:
            await ctx.message.add_reaction('\U0000274c')
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Danbooru(bot))
