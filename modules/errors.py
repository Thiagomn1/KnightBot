import discord
from discord.ext import commands

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("This command doesn't exist. Please use .help for a list of available commands.")

def setup(client):
    client.add_cog(Mod(client))