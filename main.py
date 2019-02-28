import json

import discord
from discord.ext import commands

# Put your token in a file called config.json, if you want to self-host
with open('config.json') as file:
    config = json.load(file)


async def get_prefix(_bot, message):
    prefixes = ['rin ']

    return commands.when_mentioned_or(*prefixes)(_bot, message)

extensions =['modules.API.rin_danbooru',
              'modules.API.rin_zerochan',
              'modules.discord.moderation',
              'modules.utils.errors',
              'modules.utils.information']

bot = commands.Bot(command_prefix=get_prefix)

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Loaded {extension}!')
        except discord.ClientException:
            print(f'{extension} does not have a setup...')
        except (ImportError, Exception):
            print(f'Failed to load {extension}...')


@bot.event
async def on_ready():
    print(f'Hello World, I\'m {bot.user.name}!')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('In development!'))

bot.load_extension('jishaku')
bot.run(config['token'])
