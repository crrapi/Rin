import discord
from discord.ext import commands


def check_amount(amount: int):
    if amount < 0 or amount > 500:
        raise commands.errors.BadArgument('Input a value higher than 0 and less than 500.')


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['delete', 'del'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, amount: int, member: discord.Member = None):
        """Delete messages by ammount"""
        exceptions = (commands.errors.BadArgument, Exception)

        def is_member(message):
            if member:
                return message.author.id == member.id
            return True

        try:
            check_amount(amount)
            await ctx.message.delete()
            deleted_messages = await ctx.message.channel.purge(limit=amount, check=is_member)
            await ctx.send(f'Deleted {len(deleted_messages)} messages.', delete_after=5)
        except exceptions as e:
            await ctx.send(e, delete_after=5)


def setup(bot):
    bot.add_cog(Moderation(bot))
