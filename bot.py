import discord
import os
from discord.ext import commands
from constants import TOKEN

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

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

@client.command()
async def load(ctx, extension):
    client.load_extension(f'modules.{extension}')
    await ctx.message.delete()

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'modules.{extension}')
    await ctx.message.delete()

for modules in os.listdir('./modules'):
    if modules.endswith('.py'):
        client.load_extension(f'modules.{modules[:-3]}')


client.run(TOKEN)