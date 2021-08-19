import discord
import os
import aiosqlite
import asyncio
from discord.ext import commands
from constants import TOKEN

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', intents = intents)

async def connection():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect('Data.db')
    await client.db.execute('CREATE TABLE IF NOT EXISTS rpData (user_id TEXT, character TEXT, job, PRIMARY KEY (user_id))')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Kupo!'))
    print('Bot is running.')

@client.event
async def on_member_join(member):
    channel = client.get_channel(763128481726332958)
    pfp = member.avatar_url
    embed = discord.Embed(
        title = f'Welcome to Saints Annointed, {member.name}!',
        description = 'Please take the time to set your desired roles in the server and read the rules.\nEnjoy your stay.',
        colour = discord.Colour.blue()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/875751399516958782/875770055932137482/EmbedImage.png")
    embed.set_thumbnail(url=(pfp))

    await channel.send(embed=embed)

for modules in os.listdir('./modules'):
    if modules.endswith('.py'):
        client.load_extension(f'modules.{modules[:-3]}')

client.loop.create_task(connection())
client.run(TOKEN)
asyncio.run(client.db.close())