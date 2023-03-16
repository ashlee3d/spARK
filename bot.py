import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

client.run(TOKEN)