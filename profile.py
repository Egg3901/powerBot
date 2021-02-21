from discord.ext import commands
from commonFunctions import power_url
from dotenv import load_dotenv
from commonFunctions import *
import discord
import random


load_dotenv()


client = discord.Client()


class Profiles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ This class contains registration and profile commands.
        """

    pb = commands.Bot(command_prefix=['!', '.'])

    @pb.command(pass_context=True)
    async def profile(self, ctx, user_parameter=None):
        """Fetches a power profile.
            !profile -> fetches your own profile (if registered)
            !profile <id> fetches the profile of a given id
            !profile <link> fetches the profile of a given link     not implemented
            !profile <name> fetches profile by name
            !profile <mention> fetches profile by mention
        """
        if user_parameter is None:
            print('id is none')
            user_parameter = ctx.message.author.id
            pid = query(user_parameter)[0]["power_user"]

        elif user_parameter.lower() in ["random", "rand", "r", "roulette"]:
            pid = random.randint(11,10000)
        else:
            pid = user_parameter
        print(pid)
        login_to_power(login_data, f"{power_url}/login.php")
        profile_url = f"{power_url}pol.php?pol={pid}"
        profile_page = scrape(profile_url)
        embed = parse_profile_information(profile_page, profile_url)
        await ctx.send(embed=embed)

    @pb.command(pass_context=True)
    async def register(self, ctx, user_parameter, mentioned_id=None):
        """Register yourself or (not implemented) another user ex. !register 6800 registers your ID as 6800"""
        if mentioned_id is None:
            try:
                user_parameter = int(user_parameter)
            except Exception as e:
                raise e
            user_id = ctx.message.author.id
            register(user_id, user_parameter)
            await ctx.send(embed=msgs(f"{ctx.message.author.name} registered!",
                                      f"User saved to db with id {user_parameter}")
                           )

        else:

            user_id = int(user_parameter[:-1][3:])  # formats from <!333052320252297216> to 333052320252297216
            name = ctx.message.guild.get_member(user_id).name
            register(user_id, user_parameter)
            await ctx.send(
                embed=msgs(f"{name} registered!",
                           f"User saved to db with id {user_parameter}")
            )






def setup(pb):
    pb.add_cog(Profiles(pb))
