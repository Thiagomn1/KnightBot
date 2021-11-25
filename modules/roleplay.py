import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import textwrap
import requests

class Roleplay(commands.Cog):

    def __init__(self, client):
        self.client = client
     
    # XIV
    @commands.command()
    async def rp(self, ctx, *, message):

        userid = ctx.author.id
        guildid = ctx.guild.id
        cursor = await self.client.db.execute('SELECT xiv_character FROM rpData WHERE guild = ? AND user_id = ?', (guildid, userid))
        namedb = await cursor.fetchone()

        img = Image.open(requests.get("https://cdn.discordapp.com/attachments/879812200301199423/879815069557456916/XIVDialogue1.png", stream=True).raw)
        draw = ImageDraw.Draw(img)
        titlefont = ImageFont.truetype(font="assets/MyriadSemiBold.OTF", size=40)
        dialoguefont = ImageFont.truetype(font="assets/MyriadRegular.OTF", size=36)
        buffer = BytesIO()


        if namedb is None:
            
            if (message.find("||") != -1 or message.find("|") == -1):
                await ctx.message.add_reaction(emoji='❌')
                return

            name, message = message.split('|', 1)

            draw.text((95,30), name, font=titlefont, fill=(255, 255, 255))
            textwrapped = textwrap.wrap(message, width=49)
            draw.text((55,80), '\n'.join(textwrapped), font=dialoguefont, fill=(0, 0, 0))  

            img.save(buffer, 'PNG')
            buffer.seek(0)
            await ctx.send(file = discord.File(fp=buffer, filename=f'{name}.png'))

            await ctx.message.delete()
        
        elif namedb is not None:

            if (message.find("||") != -1 or message.find("|") == -1):

                draw.text((95,30), namedb[0], font=titlefont, fill=(255, 255, 255))
                textwrapped = textwrap.wrap(message, width=49)
                draw.text((55,80), '\n'.join(textwrapped), font=dialoguefont, fill=(0, 0, 0))  

                img.save(buffer, 'PNG')
                buffer.seek(0)
                await ctx.send(file = discord.File(fp=buffer, filename=f'{namedb}.png'))

                await ctx.message.delete()

            else:

                name, message = message.split('|', 1)

                draw.text((95,30), name, font=titlefont, fill=(255, 255, 255))
                textwrapped = textwrap.wrap(message, width=49)
                draw.text((55,80), '\n'.join(textwrapped), font=dialoguefont, fill=(0, 0, 0))  

                img.save(buffer, 'PNG')
                buffer.seek(0)
                await ctx.send(file = discord.File(fp=buffer, filename=f'{name}.png'))

                await ctx.message.delete()
        
        await cursor.close()


    # Set default character for RP messages
    @commands.command()
    async def defchar(self, ctx, *, name):
        userid = ctx.author.id
        guildid = ctx.guild.id

        if len(name) > 25:
            await ctx.message.add_reaction(emoji='❌')
            return

        character = await self.client.db.execute('SELECT xiv_character FROM rpData WHERE guild = ? AND user_id = ?', (guildid, userid))
        characterdb = await character.fetchone()

        if characterdb is None:
     
            cursor = await self.client.db.execute('INSERT INTO rpData (guild, user_id, xiv_character) VALUES (?, ?, ?)', (guildid, userid, name))

        if characterdb is not None:
            
            cursor = await self.client.db.execute('UPDATE rpData SET xiv_character = ? WHERE guild = ? AND user_id = ?', (name, guildid, userid))


        await self.client.db.commit()
        await cursor.close()
        await ctx.message.add_reaction(emoji='✔')


    # Set a default job. Currently does nothing besides adding it to the database
    @commands.command()
    async def rpjob(self, ctx, job):

        if job not in ('PLD', 'WAR', 'DRK', 'GNB', 'WHM', 'SCH', 'AST', 'BLM', 'SMN', 'RDM', 'BLU', 'BRD', 'DNC', 'MCH', 'DRG', 'NIN', 'MNK', 'SAM',):
            await ctx.message.add_reaction(emoji='❌')
            return
            
        userid = ctx.author.id
        guildid = ctx.guild.id
        member = ctx.author.name
        jobicon = discord.File(f'./assets/Jobs/{job}.png', filename=f'{job}.png')


        rpjob = await self.client.db.execute('SELECT job FROM rpData WHERE guild = ? AND user_id = ?', (guildid,userid))
        jobdb = await rpjob.fetchone()

        if jobdb is None:    

            cursor = await self.client.db.execute('INSERT OR IGNORE INTO rpData (guild, user_id, job) VALUES (?, ?, ?)', (guildid, userid, job))

        if jobdb is not None:

            cursor = await self.client.db.execute('UPDATE rpData SET job = ? WHERE guild = ? AND user_id = ?', (job, guildid, userid))

        embed = discord.Embed(
        title = f'{member}',
        description = f'Your job was successfully set to {job}',
        colour = discord.Colour.red()
    )
        embed.set_thumbnail(url=(f'attachment://{job}.png'))

        await ctx.send(embed=embed, file=jobicon)
        await ctx.message.delete()
        await self.client.db.commit()
        await cursor.close()


    # FGO
    @commands.command()
    async def fgo(self, ctx, *, message):

        if (message.find("||") != -1 or message.find("|") == -1):
            await ctx.message.add_reaction(emoji='❌')
            return

        img = Image.open(requests.get("https://cdn.discordapp.com/attachments/879812200301199423/879814854444204092/FGODialogue.png", stream=True).raw)
        draw = ImageDraw.Draw(img)
        titlefont = ImageFont.truetype(font="assets/MyriadSemiBold.OTF", size=40)
        dialoguefont = ImageFont.truetype(font="assets/MyriadRegular.OTF", size=36)
        buffer = BytesIO()
    

        name, message = message.split('|', 1)

        draw.text((45,17), name, font=titlefont, fill=(255, 255, 255))
        textwrapped = textwrap.wrap(message, width=80)
        draw.text((28,75), '\n'.join(textwrapped), font=dialoguefont, fill=(255, 255, 255))  

        img.save(buffer, 'PNG')
        buffer.seek(0)
        await ctx.send(file = discord.File(fp=buffer, filename=f'{name}.png'))

        await ctx.message.delete()

def setup(client):
    client.add_cog(Roleplay(client))