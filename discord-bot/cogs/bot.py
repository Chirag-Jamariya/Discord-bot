import discord
from discord.ext import commands

class BotCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    

    async def addchannel(self, ctx, channel: discord.TextChannel):
        cursor = await self.client.db.cursor()
    
        # Check if the channel already exists in the database
        await cursor.execute("SELECT channel_id FROM channelid WHERE channel_id = ?", (channel.id,))
        result = await cursor.fetchone()
    
        if result is not None:
            return await ctx.send("This channel ID is already in the list.")
    
        # Insert the new channel ID
        await cursor.execute("INSERT INTO channelid (channel_id) VALUES (?)", (channel.id,))
        await self.client.db.commit()
    
        await ctx.send(f"Channel ID {channel.id} has been added to the database.")

async def setup(client):
    await client.add_cog(BotCog(client))