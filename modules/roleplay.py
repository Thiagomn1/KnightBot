import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import textwrap
import requests

class Roleplay(commands.Cog):

    def __init__(self, client):
        self.client = client
     
    @commands.command()
    async def rp(self, ctx, *, message):

        if (message.find("||") != -1 or message.find("|") == -1):
            await ctx.message.add_reaction(emoji='❌')
            return

        name, message = message.split('|', 1)

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

    @commands.command()
    async def defchar(self, ctx, *, name):
        userid = ctx.author.id
        cursor = await self.client.db.execute('INSERT OR IGNORE INTO rpData (user_id, character) VALUES (?, ?)', (userid, name))

        if cursor.rowcount == 0:
            await self.client.db.execute('UPDATE rpData SET character = ? WHERE user_id = ?', (name, ctx.author.id))

        await self.client.db.commit()
        await cursor.close()

        await ctx.message.add_reaction(emoji='✔')

    @commands.command()
    async def rpjob(self, ctx, job):

        if job not in ('PLD', 'WAR', 'DRK', 'GNB', 'WHM', 'SCH', 'AST', 'BLM', 'SMN', 'RDM', 'BLU', 'BRD', 'DNC', 'MCH', 'DRG', 'NIN', 'MNK', 'SAM',):
            await ctx.message.add_reaction(emoji='❌')
            return
            
        userid = ctx.author.id
        member = ctx.author.name
        jobicon = discord.File(f'./assets/Jobs/{job}.png', filename=f'{job}.png')
        cursor = await self.client.db.execute('INSERT OR IGNORE INTO rpData (user_id, job) VALUES (?, ?)', (userid, job))

        if cursor.rowcount == 0:
            await self.client.db.execute('UPDATE rpData SET job = ? WHERE user_id = ?', (job, ctx.author.id))

        embed = discord.Embed(
        title = f'{member}',
        description = f'Your job was successfully set to {job}',
        colour = discord.Colour.red()
    )
        embed.set_thumbnail(url=(f'attachment://{job}.png'))

        await ctx.send(embed=embed, file=jobicon)

        await self.client.db.commit()
        await cursor.close()

    # @commands.command()
    # async def rptest(self, ctx, *, message):

    #     userid = str(ctx.author.id)
    #     cursor = await self.client.db.execute('SELECT character FROM rpData WHERE user_id = ?', userid)

    #     if cursor is None:
    #         print('Not found')

    #     else:
    #         await ctx.send(cursor)

    #     await cursor.close()


def setup(client):
    client.add_cog(Roleplay(client))