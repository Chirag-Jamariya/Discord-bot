import discord, aiosqlite
from discord.ext import commands, tasks
import ctf
import hackathon


intents = discord.Intents.default()
intents.message_content = True  

client = commands.Bot(command_prefix='%', intents=intents)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='%', intents=intents)
        self.db = None

    async def setup_hook(self):
        self.db = await aiosqlite.connect("Main.db")
        async with self.db.cursor() as c:
            await c.execute("CREATE TABLE IF NOT EXISTS channelid(channel_id INTEGER)")
        await self.db.commit()
        
        await self.load_extension('cogs.bot')
        print("Cog 'bot' has been loaded")

    async def close(self):
        if self.db:
            await self.db.close()
        await super().close()

client = MyBot()


@client.event
async def on_ready():
    print("this bot is wrking")
    print("------------------")
    client.db= await  aiosqlite.connect("Main.db")
    c = await client.db.cursor()
    await c.execute("Create Table If Not Exists channelid(channel_id INTEGER)")
    await client.db.commit()
    post_ctf_info.start()
    hackathon_info.start()
    

@client.command()
async def hello1(ctx):
    await ctx.send("hello, i am made to provide you with upcoming ctfs and hackathons")


@client.command()
async def info(ctx):
    await ctx.send("this bot will give info about upcoming ctfs and hackathons \n use  **%ctf_info** to know about upcoming ctf events \n use **%hackathon_info** to know abut upcoming hackathons event ")

@tasks.loop(hours=24)
async def post_ctf_info():
    print("Posting CTFs")
    upcomingctfs = ctf.get_upcoming_ctfs()
    
    if not upcomingctfs:
        message = "No upcoming CTFs found."
    else:
        message = "**Upcoming CTFs:**\n"
        for ct in upcomingctfs[:5]:  
            title = ct["title"]
            start_time = ct.get('start', 'NA')  
            ctf_format = ct.get('format', 'NA')  
            url = f"https://ctftime.org/event/{ct['id']}"
            message += f"**- Name: {title}\n**"
            message += f"  Start Time: {start_time}\n"
            message += f"  Format: {ctf_format}\n"
            message += f"  URL: <{url}>\n\n"
    
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT channel_id FROM channelid")
        channels = await cursor.fetchall()
    
    for channel_id in channels:
        channel = client.get_channel(channel_id[0])
        if channel:
            try:
                await channel.send(message)
                print(f"Sent CTF info to channel: {channel.name} ({channel.id})")
            except discord.errors.Forbidden:
                print(f"No permission to send messages in channel: {channel.name} ({channel.id})")
            except Exception as e:
                print(f"Error sending message to channel {channel.id}: {str(e)}")
        else:
            print(f"Channel not found: {channel_id[0]}")


@tasks.loop(hours=24)
async def hackathon_info():
    print("posting hackathon")
    upcominghack=hackathon.get_upcoming_hackathons()['hackathons']
    if not upcominghack:
        message="No upcoming hackathons found."
        return
    else:
        message = "**Upcoming Hackathons:**\n\n"
        for hk in upcominghack[:5]:  
            title = hk["title"]
            url   = hk["url"] 
            submission_period = hk["submission_period_dates"]
            time_left = hk["time_left_to_submission"]
            candidates = hk["registrations_count"]
        
            message += f"**- Name: {title}\n**"
            message += f"- Submission Period Date: {submission_period}\n"
            message += f"- Time left: {time_left}\n"
            message += f"- Total candidates: {candidates}\n"
            message += f"- URL: <{url}>\n\n "
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT channel_id FROM channelid")
        channels = await cursor.fetchall()
    for channel_id in channels:
        channel = client.get_channel(channel_id[0])
        if channel:
            try:
                await channel.send(message)
                print(f"Sent CTF info to channel: {channel.name} ({channel.id})")
            except discord.errors.Forbidden:
                print(f"No permission to send messages in channel: {channel.name} ({channel.id})")
            except Exception as e:
                print(f"Error sending message to channel {channel.id}: {str(e)}")
        else:
            print(f"Channel not found: {channel_id[0]}")
    await channel.send(message)

client.run('Your discord bot token')  