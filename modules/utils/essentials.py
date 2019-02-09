import discord

from discord.ext import commands

from .paginator import HelpPaginator


class Essentials:
    """Essentials commands for bot usage"""

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(name='help')
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
    async def ping(self, ctx):
        """Sends bot latency in ms"""
        await ctx.send(f'Ping: {round(self.bot.latency * 1000, 2)} ms')

    @commands.command(aliases=['i'])
    async def info(self, ctx):
        """Sends bot info"""
        embed = discord.Embed(color=discord.Colour.red(), title='Info')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/' +
                '540345349576065065/' +
                'c3dc0a076be76b5690ca69ddcd14c465.png')
        embed.add_field(name="Owner", value="reformed#5680", inline=True)
        embed.add_field(name="Prefix", value="rin", inline=True)
        embed.add_field(name="Library", value="discord.py [rewrite]", inline=True)
        embed.add_field(name="Ping", value=f'{round(self.bot.latency * 1000, 2)} ms', inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Essentials(bot))
