from discord.ext import commands


class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f'This is not a command...')

        elif isinstance(error, commands.UserInputError):
            return await ctx.send('Use a valid input instead.')

        elif isinstance(error, commands.NotOwner):
            return await ctx.message.add_reaction('\U0001f6ab')

        elif isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            return await ctx.send(f'Try again in {seconds:.2f} seconds!')


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
