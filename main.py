import discord
from json import load
from discord.ext import commands

with open('config.json') as file:
    config = load(file)

async def get_prefix(bot, message):
    
    prefixes = ['u?', 'u!']

    if not message.guild:
        return '?'
    
    return commands.when_mentioned_or(*prefixes)(bot, message)

extensions = ['modules.API.rin-zerochan']

bot = commands.Bot(command_prefix=get_prefix)

if __name__ == '__main__':
    for extension in extensions:
        try:
            print(f'Loading {extension}...')
            bot.load_extension(extension)
        except:
            print(f'Failed to load extension {extension}')

@bot.event
async def on_ready():
    print(f'Hello World, I\'m {bot.user.name}')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Being code by reformed#5680'))

bot.load_extension('jishaku')
bot.run(config['token'])