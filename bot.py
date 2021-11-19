import discord
import os
import aiosqlite
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', intents = intents)
token = os.environ["TOKEN"]

async def connection():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect('Database.db')
    await client.db.execute('CREATE TABLE IF NOT EXISTS modData (guild_id TEXT, welcome TEXT, PRIMARY KEY (guild_id))')
    await client.db.execute('CREATE TABLE IF NOT EXISTS rpData (guild TEXT, user_id TEXT, xiv_character TEXT, job TEXT, FOREIGN KEY(guild) REFERENCES modData(guild_id))');


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Roleplaying'))
    print('Bot is running.')

@client.event
async def on_guild_join(guild):
    await client.db.execute('INSERT OR IGNORE INTO modData (guild_id) VALUES (?)', (guild.id,))
    await client.db.commit()

@client.event
async def on_guild_remove(guild):
    await client.db.execute('DELETE FROM modData WHERE guild_id = ?', (guild.id,))
    await client.db.execute('DELETE FROM rpData WHERE guild_id = ?', (guild.id,))
    await client.db.commit()

@client.event
async def on_member_join(member):
    guild = member.guild
    cursor = await client.db.execute('SELECT welcome FROM modData WHERE guild_id = ?', (member.guild.id,))
    message = await cursor.fetchone()

    if guild.system_channel is not None:
            
        pfp = member.avatar_url
        embed = discord.Embed(
            title = f'Welcome to {member.guild.name}, {member.name}!',
            description = f'{message}',
            colour = discord.Colour.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/875751399516958782/875770055932137482/EmbedImage.png")
        embed.set_thumbnail(url=(pfp))

        await guild.system_channel.send(embed=embed)


for modules in os.listdir('./modules'):
    if modules.endswith('.py'):
        client.load_extension(f'modules.{modules[:-3]}')

client.loop.create_task(connection())
client.run(token)
asyncio.run(client.db.close())