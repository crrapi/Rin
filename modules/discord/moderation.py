from discord.ext import commands


def check_amount(amount):
    if amount is None:
        raise commands.UserInputError('Input a amount of messages that you want to be deleted.')
    if amount < 0 or amount > 500:
        raise commands.BadArgument('Input a amount that is higher than 0 or less than 500.')

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['delete', 'del'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, amount: int = None):
        """Delete messages by ammount"""
        exceptions = (commands.UserInputError, commands.BadArgument)
        try:
            check_amount(amount)
            await ctx.message.delete()
            await ctx.message.channel.purge(limit=amount)
            await ctx.send(f'Deleted {int(amount)} messages.', delete_after=5)
        except exceptions as e:
            await ctx.send(e)

    @purge.error
    async def purge_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have Manage Messages permission to do that.')
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send('I dont have Manage Messages permission to do that.')

def setup(bot):
    bot.add_cog(Moderation(bot))
