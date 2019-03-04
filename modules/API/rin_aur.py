import aiohttp
import discord
from discord.ext import commands
from ..utils.paginator import Pages


class AUR(commands.Cog):
    """Commands for Aurweb RPC Integration"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['aurweb', 'rpc'])
    @commands.is_owner()
    async def aur(self, ctx, *, query: str):
        """Search packages from AUR"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://aur.archlinux.org/rpc/?v=5&type=search&arg={query}') as response:
                response = await response.json()
                response = response['results']
                names = [i['Name'] for i in response]
                pages = Pages(ctx, lines=tuple(names))
                await pages.paginate()


def setup(bot):
    bot.add_cog(AUR(bot))
