from random import choice, randint
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
        try:
            query.lower()
            client = DB('danbooru')
            if 'rating' in query:
                raise custom_exceptions.NSFWException('Good try, pervy!')
            post = client.post_list(tags='rating:safe ' + query, page=randint(1, 1000), limit=1)
            image_url = choice(post)['file_url']
            if not image_url:
                raise custom_exceptions.ImageNotFound('Image not found')
            embed = Embed(color=Colour.red())
            embed.set_image(url=image_url)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except (custom_exceptions.NSFWException, custom_exceptions.ImageNotFound, Exception) as e:
            await ctx.send(e)

    @danbooru.command(aliases=['n'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def nsfw(selfs, ctx, *, query: str):
        """Connects with Danbooru client and retrieve a random image
        from a post list (only NSFW channels)."""
        try:
            query.lower()
            if not ctx.channel.nsfw:
                raise custom_exceptions.NSFWException('NSFW commands only in NSFW channels!')
            client = DB('danbooru')
            post = client.post_list(tags=query, page=randint(1, 1000), limit=1)
            image_url = choice(post)['file_url']
            if not image_url:
                raise custom_exceptions.ImageNotFound('Image not found.')
            embed = Embed(color=Colour.red())
            embed.set_image(url=image_url)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except (custom_exceptions.NSFWException, custom_exceptions.ImageNotFound, Exception) as e:
            await ctx.send(e)

    @danbooru.command(aliases=['t'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def tags(self, ctx, *, match: str):
        """Retrieves tags that matches you query."""
        try:
            match.lower()
            client = DB('danbooru')
            list_tags = client.tag_list(name_matches=match)
            related_tags = [i['related_tags'] for i in list_tags]
            if not related_tags:
                raise custom_exceptions.TagsNotFound('Tags not found.')
            tags = sub(r'[0-9.]+', '', ''.join(related_tags))
            pages = Pages(ctx, lines=tuple(tags.split()))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except (custom_exceptions.TagsNotFound, Exception) as e:
            await ctx.send(e)

    @danbooru.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def pool(self, ctx, *, match: str):
        """Retrieve pool names and id from your query."""
        try:
            match.lower()
            client = DB('danbooru')
            pool_list = client.pool_list(name_matches=match)
            if not pool_list:
                raise custom_exceptions.PoolNotFound('Pool not found.')
            names = [i['name'] for i in pool_list]
            ids = [i['id'] for i in pool_list]
            names_ids = list(zip(names, ids))
            pages = Pages(ctx, lines=names_ids)
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except (custom_exceptions.PoolNotFound, Exception) as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Danbooru(bot))
