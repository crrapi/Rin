from discord.ext import commands

class Owner:
    """Owner commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['die', 'kys'])
    @commands.is_owner()
    async def logout(self, ctx):
        """Stop the process that bot's running"""
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
