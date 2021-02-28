from discord.ext import commands
from common.common_functions import *


class UpdateRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ This class contains registration and profile commands.
        """

    pb = commands.Bot(command_prefix=['!', '.'])

    @pb.command(pass_context=True, aliases=["roles"])
    @commands.has_any_role("Strategist", "Bot Master", "Verified", "Politburo Member", "International Affairs Chair")
    async def update_roles(self, ctx):
        print(db)
        users = db.all()
        print(str(users))
        await ctx.send(embed=msgs(f" updated!",
                                  f"User saved to db with id {users}")
                       )
        for user in users:
            discord_id = user["discord_user"]
            power_id = user["power_user"]
            await ctx.send(embed=msgs(f"{discord_id} updated!",
                                      f"User saved to db with id {power_id}")
                           )


def setup(pb):
    pb.add_cog(UpdateRoles(pb))





