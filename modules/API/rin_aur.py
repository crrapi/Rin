import aiohttp
from discord.ext import commands

from ..utils import custom_exceptions
from ..utils.paginator import Pages


class AUR(commands.Cog):
    """Commands for Aurweb RPC Integration"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['aurweb', 'rpc'])
    async def aur(self, ctx, *, query: str):
        """Search packages from AUR"""
        query = query.lower()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://aur.archlinux.org/rpc/?v=5&type=search&arg={query}') as response:
                exceptions = (custom_exceptions.ResourceNotFound, Exception)
                try:
                    response = await response.json()
                    response = response['results']
                    if not response:
                        raise custom_exceptions.ResourceNotFound('Results not found.')
                    names = [i['Name'] for i in response]
                    pages = Pages(ctx, lines=tuple(names))
                    await pages.paginate()
                except exceptions as e:
                    await ctx.message.add_reaction('\U0000274c')
                    await ctx.send(e, delete_after=10)


def setup(bot):
    bot.add_cog(AUR(bot))
