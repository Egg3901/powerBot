import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
"""Programmed by Egg"""

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # fetches discord token from your environment


client = discord.Client()
pb = commands.Bot(command_prefix=['!', '.'])
"""The cogs to be loaded by the bot"""
cogs = [
        'profile',
        'race_tracker'
]


@pb.event
async def on_ready():
    """This event triggers on client connection to discord"""
    print(f'{pb.user} is ready')
    await pb.change_presence(activity=discord.Game(name="Socialism is when the government does stuff"))
if __name__ == '__main__':
    for cog in cogs:
        try:
            pb.load_extension(cog)
            print(f'Loaded {cog}!')
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
            pass

pb.run(TOKEN)
