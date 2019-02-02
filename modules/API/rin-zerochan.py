from ..utils.paginator import Pages
from aiohttp import ClientSession
from random import choice, randint
from discord import Embed, Colour
from discord.ext import commands

class ZeroChan:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(aliases=['zc'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def zerochan(self, ctx, *, query: str, pages = randint(0, 11)):
        '''Search images from ZeroChan (random)'''
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/search/{query}/{pages}') as response:
                try:
                    data = (await response.json())['data']
                    embed = Embed(color=Colour.red())
                    random_image = choice(data)['thumb']
                    embed.set_image(url=random_image)
                    await ctx.send(embed=embed)
                except Exception as e:
                    await ctx.send(e)
                
    @zerochan.command(aliases=['i'], pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def image(self, ctx, id: str):
        '''Search images by ID'''
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/image/{id}') as response:
                try:
                    data = (await response.json())['data']
                    image = data['url']
                    await ctx.send(image)
                except:
                    await ctx.send('Image not found')
    
    @zerochan.command(aliases=['info', 'in'], pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def information(self, ctx, *, query: str):
        '''Get info from tags'''
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/info/{query}') as response:
                try:
                    info = (await response.json())['data']
                    await ctx.send(info)
                except:
                    await ctx.send('Info not found')
    
    @zerochan.command(aliases=['m'], pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def meta(self, ctx, *, query: str):
        '''Get tags' names from meta'''
        async with ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/meta/{query}') as response:
                data = (await response.json())['data']
                p = Pages(ctx, entries=tuple(i['name'] for i in data))
                await p.paginate()

def setup(bot):
    bot.add_cog(ZeroChan(bot))
