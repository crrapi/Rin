from random import randint
from re import sub

from discord import Colour, Embed
from discord.ext import commands
from pybooru import Danbooru as DB

from ..utils import custom_exceptions
from ..utils.paginator import Pages


class Danbooru:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['db'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def danbooru(self, ctx, *, query: str):
        """Connects with the Danbooru client and retrieve a random image
        from a post list (only SFW channels)."""
        exceptions = custom_exceptions.NSFWException, custom_exceptions.ResourceNotFound, Exception
        try:
            query.lower()
            client = DB('danbooru')
            if 'rating' in query:
                raise custom_exceptions.NSFWException('Good try, pervy!')
            post = client.post_list(tags='rating:safe ' + query, page=randint(1, 1000), limit=1)
            if not post:
                raise custom_exceptions.ResourceNotFound('Image not found.')
            image_url = post[0]['file_url']
            embed = Embed(color=Colour.red())
            embed.description = f'[Source]({image_url})'
            embed.set_image(url=image_url)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except (exceptions) as e:
            await ctx.send(e)

    @danbooru.command(aliases=['n'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def nsfw(selfs, ctx, *, query: str):
        """Connects with Danbooru client and retrieve a random image
        from a post list (only NSFW channels)."""
        exceptions = custom_exceptions.NSFWException, custom_exceptions.ResourceNotFound, Exception
        try:
            query.lower()
            if not ctx.channel.nsfw:
                raise custom_exceptions.NSFWException('NSFW commands only in NSFW channels!')
            client = DB('danbooru')
            post = client.post_list(tags=query, page=randint(1, 1000), limit=1)
            if not post:
                raise custom_exceptions.ResourceNotFound('Image not found.')
            image_url = post[0]['file_url']
            embed = Embed(color=Colour.red())
            embed.description = f'[Source]({image_url})'
            embed.set_image(url=image_url)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except (exceptions) as e:
            await ctx.send(e)

    @danbooru.command(aliases=['t'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def tags(self, ctx, *, match: str):
        """Retrieves tags that matches you query."""
        exceptions = custom_exceptions.ResourceNotFound, Exception
        try:
            match.lower()
            client = DB('danbooru')
            list_tags = client.tag_list(name_matches=match)
            related_tags = [i['related_tags'] for i in list_tags]
            if not related_tags:
                raise custom_exceptions.ResourceNotFound('Tags not found.')
            tags = sub(r'[0-9.]+', '', ''.join(related_tags))
            pages = Pages(ctx, lines=tuple(tags.split()))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except (exceptions) as e:
            await ctx.send(e)

    @danbooru.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def pool(self, ctx, *, match: str):
        """Retrieve pool names and id from your query."""
        exceptions = custom_exceptions.ResourceNotFound, Exception
        try:
            match.lower()
            client = DB('danbooru')
            pool_list = client.pool_list(name_matches=match)
            if not pool_list:
                raise custom_exceptions.ResourceNotFound('Pool not found.')
            names = [i['name'] for i in pool_list]
            ids = [i['id'] for i in pool_list]
            names_ids = list(zip(names, ids))
            pages = Pages(ctx, lines=names_ids)
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except (exceptions) as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Danbooru(bot))
