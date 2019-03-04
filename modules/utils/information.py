import discord
import humanize
import psutil
import sys
from discord.ext import commands

from .paginator import HelpPaginator


def get_cpu_usage():
    proc = psutil.Process()
    cpu = proc.cpu_percent()
    return cpu


def get_mem_usage():
    proc = psutil.Process()
    mem = proc.memory_full_info().uss
    return humanize.naturalsize(mem)


class Information(commands.Cog):
    """Commands for bot information"""

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(name='help')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _help(self, ctx, *, command: str = None):
        """All commands support"""
        global pages
        try:
            if command is None:
                pages = await HelpPaginator.from_bot(ctx)
            else:
                specific = self.bot.get_cog(command) or self.bot.get_command(command)

                if specific is None:
                    await ctx.send('Command not found.')
                elif isinstance(specific, commands.Command):
                    pages = await HelpPaginator.from_command(ctx, specific)
                else:
                    pages = await HelpPaginator.from_cog(ctx, specific)
            await pages.paginate()
        except Exception as e:
            await ctx.send(e)

    @commands.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """Sends bot latency in ms"""
        await ctx.send(f'Ping: {round(self.bot.latency * 1000, 2)} ms')

    @commands.command(aliases=['i'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        """Sends bot info"""
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/' +
                '540345349576065065/' +
                'c3dc0a076be76b5690ca69ddcd14c465.png')
        embed.add_field(name='Name', value='Rin', inline=True)
        embed.add_field(name='Owner', value='reformed#5680', inline=True)
        embed.add_field(name='Python Version', value=f'{sys.version[:5]}', inline=True)
        embed.add_field(name='Library', value='discord.py [rewrite]', inline=True)
        embed.add_field(name='Prefix', value='rin', inline=True)
        embed.add_field(name='Source', value='[GitHub](https://github.com/ArK7652/Rin)', inline=True)
        embed.add_field(name='Support', value='[Server](https://discord.gg/tdVZsDv)', inline=True)
        embed.add_field(name='Bot Invite',
                        value='[Invite](https://discordapp.com/oauth2/authorize?' +
                              'client_id=545661874809864233&scope' +
                              '=bot&permissions=0)',
                        inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['u'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def usage(self, ctx):
        """Currently usage of this python process"""
        embed = discord.Embed(color=discord.Colour.red())
        embed.add_field(name='CPU', value=f'{get_cpu_usage()}%')
        embed.add_field(name='RAM', value=f'{get_mem_usage()}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
