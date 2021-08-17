import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import textwrap
import requests
import os

class Roleplay(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rp(self, ctx, *, message):

        if (message.find("||") != -1 or message.find("|") == -1):
            await ctx.message.add_reaction(emoji='❌')
            
        else:
            name, message = message.split('|')

            img = Image.open(requests.get("https://cdn.discordapp.com/attachments/876184454232686592/876499856653418526/Dialogue.png", stream=True).raw)
            draw = ImageDraw.Draw(img)
            titlefont = ImageFont.truetype(font="assets/MyriadSemiBold.otf", size=18)
            dialoguefont = ImageFont.truetype(font="assets/MyriadRegular.otf", size=16)
            buffer = BytesIO()

            draw.text((45,13), name, font=titlefont, fill=(255, 255, 255))
            textwrapped = textwrap.wrap(message, width=70)
            draw.text((28,40), '\n'.join(textwrapped), font=dialoguefont, fill=(0, 0, 0))  

            img.save(buffer, 'PNG')
            buffer.seek(0)
            await ctx.send(file = discord.File(fp=buffer, filename=f'{name}.png'))

            await ctx.message.delete()

    @rp.error
    async def rp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction(emoji='❌')


def setup(client):
    client.add_cog(Roleplay(client))