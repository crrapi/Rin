from discord.ext import commands

from .paginator import HelpPaginator


class Essentials:
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(name='help')
    async def _help(self, ctx, *, command: str = None):
        """All commands support"""

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
        """Send bot latency in ms"""
        await ctx.send(f'Ping: {round(self.bot.latency * 1000, 2)}')

def setup(bot):
    bot.add_cog(Essentials(bot))
