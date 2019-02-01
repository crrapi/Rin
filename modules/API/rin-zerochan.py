import time
import aiohttp
import json
from random import choice
from discord.ext import commands

class ZeroChan:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='zerochan', aliases=['zc'], pass_context=True, invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def zerochan(self, ctx, *, query: str):
        '''Search images from ZeroChan'''
        async with ctx.typing(), aiohttp.ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/search/{query}') as response:
                try:
                    image = (await response.json())['data']
                    await ctx.send(choice(image)['thumb'])
                except:
                    await ctx.send('Image not found')
    
    @zerochan.command(name='image', aliases=['i'], pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def image(self, ctx, id: str):
        '''Search images by ID'''
        async with ctx.typing(), aiohttp.ClientSession() as session:
            async with session.post(f'https://rin-zerochan.herokuapp.com/image/{id}') as response:
                try:    
                    image = (await response.json())['data']
                    await ctx.send(image['url'])
                except:
                    await ctx.send('Image not found')

def setup(bot):
    bot.add_cog(ZeroChan(bot))