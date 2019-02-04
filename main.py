from discord import Status, Game
from json import load
from discord.ext import commands

# Put your token in a file called config.json, if you want to self-host
with open('config.json') as file:
    config = load(file)


async def get_prefix(bot, message):

    prefixes = ['u?', 'u.']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)

extensions = ['modules.utils.errors',
              'modules.API.rin-zerochan', 'modules.API.rin-danbooru']

bot = commands.Bot(command_prefix=get_prefix)

if __name__ == '__main__':
    for extension in extensions:
        try:
            print(f'Loading {extension}...')
            bot.load_extension(extension)
            print(f'Loaded {extension}!')
        except:
            print(f'Failed to load extension {extension}')


@bot.event
async def on_ready():
    print(f'Hello World, I\'m {bot.user.name}')
    await bot.change_presence(status=Status.idle, activity=Game('Being code by reformed#5680'))

bot.load_extension('jishaku')
bot.run(config['token'])
