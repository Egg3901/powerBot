import os
import discord

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #fetches discord token from your environment

client = discord.Client()


@client.event()
async def on_ready():
    print(f'{client.user} is ready')

client.run(TOKEN)