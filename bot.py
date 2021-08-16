import discord
import os
import textwrap
import requests
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
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
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    channel = client.get_channel(856021386438246420)

    await member.kick(reason=reason)
    await channel.send(f'User: {member.mention} has been kicked from the server\nReason: {reason}')
    
    await ctx.message.delete()

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    channel = client.get_channel(856021386438246420)

    await member.ban(reason=reason)
    await channel.send(f'User: {member.mention} was permanently banned from the server\nReason: {reason}')

    await ctx.message.delete()

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    channel = client.get_channel(856021386438246420)

    for banned in banned_users:
        user = banned.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await channel.send(f'User: {user.mention} was unbanned from the server')
            return

    await ctx.message.delete()

@client.command()
async def rp(ctx, *, argument):
    channel = client.get_channel(876184454232686592)

    if (argument.find("||") != -1):
        await channel.send("Incorrect usage, command should be: .rp | charactername | message")
        return
    
    elif (argument.find("|") == -1):
        await channel.send("Incorrect usage, command should be: .rp | charactername | message")
        return

    else:
        name, message = argument.split('|')

        img = Image.open(requests.get("https://cdn.discordapp.com/attachments/876184454232686592/876499856653418526/Dialogue.png", stream=True).raw)
        draw = ImageDraw.Draw(img)
        titlefont = ImageFont.truetype(font="assets/MyriadSemiBold.otf", size=18)
        dialoguefont = ImageFont.truetype(font="assets/MyriadRegular.otf", size=16)

        draw.text((45,13), name, font=titlefont, fill=(255, 255, 255))
        textwrapped = textwrap.wrap(message, width=70)
        draw.text((28,40), '\n'.join(textwrapped), font=dialoguefont, fill=(0, 0, 0))  

        img.save(f"{name}.png")
        await channel.send(file = discord.File(f"{name}.png"))
        os.remove(f"{name}.png")

        await ctx.message.delete()

client.run(TOKEN)