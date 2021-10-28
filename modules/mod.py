import discord
from discord.ext import commands

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):

        await member.kick(reason=reason)
        await ctx.send(f'User: {member.mention} has been kicked from the server\nReason: {reason}')
        
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):

        await member.ban(reason=reason)
        await ctx.send(f'User: {member.mention} was permanently banned from the server\nReason: {reason}')

        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for banned in banned_users:
            user = banned.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'User: {user.mention} was unbanned from the server')
                return

        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


    # Load/Unload Cogs
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        self.client.load_extension(f'modules.{extension}')
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'modules.{extension}')
        await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(administrator=True)
    async def welcome(self, ctx, *, message):
        guildid = ctx.guild.id

        await self.client.db.execute('UPDATE modData SET welcome = ? WHERE guild_id = ?', (message, guildid))
        await self.client.db.commit()
        
        await ctx.send(f'Welcome message was successfully set to: {message}')
        await ctx.message.delete()

def setup(client):
    client.add_cog(Mod(client))