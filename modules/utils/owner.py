from discord.ext import commands

class Owner:
    """Commands for owner only"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['die', 'kys'])
    @commands.is_owner()
    async def logout(self, ctx):
        """Stop the process that bot's running"""
        await ctx.message.add_reaction('\U0001f525')
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
