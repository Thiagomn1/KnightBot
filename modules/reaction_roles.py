import discord
from discord.ext import commands

class ReactionRole(commands.Cog):

    # Initialize and set messege/emoji IDs for reaction add
    def __init__(self, client):
        self.client = client
        self.role_message_id = 877714939173814282
        self.emoji_to_role = {      
            discord.PartialEmoji(name='🔴'): 856007661728563220,
            discord.PartialEmoji(name='🟡'): 763082110801543189,
        }


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        if payload.message_id != self.role_message_id:
            return

        guild = self.client.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        try:
            await payload.member.add_roles(role) # Add role if all conditions met

        except discord.HTTPException:
            pass


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):

        if payload.message_id != self.role_message_id:
            return

        guild = self.client.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        try:
            await member.remove_roles(role) # Remove role if all conditions met
            
        except discord.HTTPException:
            pass

     
def setup(client):
    client.add_cog(ReactionRole(client))