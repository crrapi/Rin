import sys
import traceback

from discord import errors
from discord.ext import commands

class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.NotOwner):
            return await ctx.message.add_reaction('\U0001f6ab')

        elif isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            return await ctx.send(f'Try again in {seconds:.2f} seconds!')

        elif isinstance(error, errors.HTTPException):
            return await ctx.send('Cannot send an empty message.')

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send('I don\'t have permission to do that')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
