import json
import discord
from discord.ext import commands

# Put your token in a file called config.json, if you want to self-host
with open('config.json') as file:
    config = json.load(file)

extensions = ['modules.API.rin_danbooru',
              'modules.API.rin_zerochan',
              'modules.API.rin_aur',
              'modules.discord.moderation',
              'modules.utils.errors',
              'modules.utils.information',
              'jishaku']

bot = commands.Bot(command_prefix=commands.when_mentioned_or('rin '))

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Loaded {extension}!')
        except discord.ClientException:
            print(f'{extension} does not have a setup function...')
        except (ImportError, Exception) as e:
            print(f'Failed to load {extension}... ({e})')


@bot.event
async def on_ready():
    print(f'Hello World, I\'m {bot.user.name}!')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name='In development!'))


bot.run(config['token'])
