from random import choice, randint
from re import sub

from discord import Colour, Embed
from discord.ext import commands
from pybooru import Danbooru

from ..utils.paginator import Pages


class DanbooruIntegration:
    """Commands for Danbooru integration

    Methods
    -----------
    danbooru:
        Connects with the Danbooru client and retrieve a post list
        with tags related in NSFW and SFW channels.
    tags:
        Retrieves tags that matches you query.
    pool:
        Retrieve pools names from your query.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['db'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def danbooru(self, ctx, *, query: str):
        """Connects with the Danbooru client and retrieve a post list
        with tags related in NSFW and SFW channels."""
        try:
            client = Danbooru('danbooru')
            if ctx.channel.nsfw:
                post = client.post_list(
                    tags=query, page=randint(1, 1000), limit=1)
            else:
                post = client.post_list(
                    tags='rating:safe ' + query, page=randint(1, 1000), limit=1)
            image_url = choice(post)['file_url']
            embed = Embed(color=Colour.red())
            embed.set_image(url=image_url)
            await ctx.message.add_reaction('\U00002705')
            await ctx.send(embed=embed)
        except:
            await ctx.send('Image not found.')

    @danbooru.command(aliases=['t'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def tags(self, ctx, *, match: str):
        """Retrieves tags that matches you query."""
        try:
            client = Danbooru('danbooru')
            list_tags = client.tag_list(name_matches=match)
            related_tags = [i['related_tags'] for i in list_tags]
            tags = sub(r'[0-9\.]+', '', ''.join(related_tags))
            pages = Pages(ctx, lines=tuple(tags.split()))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except Exception as e:
            await ctx.send(e)

    @danbooru.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def pool(self, ctx, *, match: str):
        """Retrieve pool names and name from your query."""
        try:
            client = Danbooru('danbooru')
            pool_list = client.pool_list(name_matches=match)
            ids = [i['names'] for i in pool_list]
            pages = Pages(ctx, lines=tuple(ids))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(DanbooruIntegration(bot))
