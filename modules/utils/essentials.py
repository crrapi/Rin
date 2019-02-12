import discord
import sys

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
        embed = discord.Embed(color=discord.Colour.red(), title='Bot information')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/' +
                '540345349576065065/' +
                'c3dc0a076be76b5690ca69ddcd14c465.png')
        embed.add_field(name='Name', value='Rin', inline=True)
        embed.add_field(name='Owner', value='reformed#5680', inline=True)
        embed.add_field(name='Python Version', value=f'{sys.version[:5]}', inline=True)
        embed.add_field(name='Library', value='discord.py [rewrite]', inline=True)
        embed.add_field(name='Prefix', value='rin', inline=True)
        embed.add_field(name='Ping', value=f'{round(self.bot.latency * 1000, 2)} ms', inline=True)
        embed.add_field(name='Support', value='[Server](https://discord.gg/HaCgM7y)', inline=True)
        embed.add_field(name='Bot Invite', value='[Invite](https://discordapp.com/api/oauth2/authorize?client_id=541341902922842133&permissions=0&scope=bot)', inline=True)
        await ctx.send(embed=embed)

@commands.command(aliases=['delete', 'p']	   @commands.has_permissions(manage_guild=True)
    async def purge(self, ctx, amount: int=None):
        """Delete messages by ammount"""
        exceptions = (commands.MissingRequiredArgument,commands.BadArgument, Exception)
        try:
        	if amount is None:
            	raise commands.MissingRequiredArgument('Missing required argument: amount')
        	if amount>500 or amount<0:
            	raise commands.BadArgument('You cant input a ammount less than 0 or higher than 500')
        	await ctx.message.delete()
        	await ctx.message.channel.purge(limit=amount)
        	await ctx.send(f'Deleted {int(amount)} messages.', delete_after=5)
		except exceptions as e:
			await ctx.send(e)

def setup(bot):
    bot.add_cog(Essentials(bot))
