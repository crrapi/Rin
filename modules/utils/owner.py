from discord.ext import commands

class Owner:
    """Owner commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['die', 'kys'])
    async def logout(self, ctx):
        """Stop the process that bot's running"""
        await ctx.invoke(self.bot.get_command('jsk'), 'py await _bot.logout()')


def setup(bot):
    bot.add_cog(Owner(bot))
