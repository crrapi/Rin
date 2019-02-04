from discord.ext import commands
from discord import Embed, Colour
from pybooru import Danbooru
from random import choice, randint
from ..utils.paginator import Pages
import re


class DanbooruCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['db'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def danbooru(self, ctx, *, tags: str):
        try:
            client = Danbooru('danbooru')
            if ctx.channel.nsfw:
                post = client.post_list(
                    tags=tags, page=randint(1, 1000), limit=1)
            else:
                post = client.post_list(
                    tags='rating:safe ' + tags, page=randint(1, 1000), limit=1)
            async with ctx.typing():
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
        try:
            client = Danbooru('danbooru')
            list_tags = client.tag_list(name_matches=match)
            related_tags = [i['related_tags'] for i in list_tags]
            tags = re.sub(r'[0-9\.]+', '', ''.join(related_tags))
            pages = Pages(ctx, lines=tuple(tags.split()))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except Exception as e:
            await ctx.send(e)

    @danbooru.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def pool(self, ctx, *, match: str):
        try:
            client = Danbooru('danbooru')
            pool_list = client.pool_list(name_matches=match)
            ids = [i['id'] for i in pool_list]
            pages = Pages(ctx, lines=tuple(ids))
            await ctx.message.add_reaction('\U00002705')
            await pages.paginate()
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(DanbooruCog(bot))
