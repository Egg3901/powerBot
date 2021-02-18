import discord
from discord.ext import commands
import os.path, time
from discord.ext.commands import Bot
import json
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

client = discord.Client()


def parse_race_data(race_data):
    race_times = []
    race_votes = []
    race_parties = {}
    n = 0
    candidate_totals = []

    for item in race_data:
        try:
            indiv_time = item[0]  # the time of this given vote total's data
            race_times.append(indiv_time)  # appends the time to the main
            vote_totals = item[1]
            total_voter_turnout = []
            for candidate in vote_totals:
                votes = candidate["voters"].replace(',', '')
                total_voter_turnout.append(float(votes))
                name = candidate["party"]
                candidate_totals.append(name)
            race_votes.append(sum(total_voter_turnout))
            n += 1
        except Exception as e:
            pass
    for i in candidate_totals:
        race_parties[i] = []
    n = 0
    for item in race_data:
        vote_totals = race_data[n][1]
        for candidate in vote_totals:
            for key in race_parties:

                party_name = str(key)

                if party_name == candidate['party']:
                    votes = candidate["voters"].replace(',', '')
                    race_parties[str(party_name)].append(votes)
                else:
                    pass
        n += 1

    return race_parties, race_times, race_votes


def update_current_total_gain(race_parties):
    current_total_gain = []
    current_total = []
    prev_total = []
    current_bd_dict = {}

    print(str(race_parties))
    for party in race_parties:
        vote_totals1 = race_parties[str(party)]
        vval1 = vote_totals1[len(vote_totals1) - 1]
        vval2 = vote_totals1[len(vote_totals1) - 2]
        gain = int(vval1) - int(vval2)
        current_total_gain.append(gain)
        current_total.append(int(vval1))
        prev_total.append(int(vval2))

    try:
        for party in race_parties:
            vote_totals1 = race_parties[str(party)]
            vval1 = vote_totals1[len(vote_totals1) - 1]
            vval2 = vote_totals1[len(vote_totals1) - 2]
            gain = int(vval1) - int(vval2)
            propgain = gain / sum(current_total_gain)

            current_bd_dict[party] = float(round(propgain * 100, 3))
        current_labels = []
        current_values = []
        for key in current_bd_dict:
            polling = round(float(current_bd_dict[key]), 2)
            current_labels.append(key)
            current_values.append(polling)
    except Exception as e:
        pass

    return current_total, prev_total, current_values, current_labels


def update_stats(race_parties):
    columns = ['Votes Last Update', 'Votes This Update', 'Change', 'Poll % This Update', ' Last Update',
               'Change in polling']
    row_labels = []
    data = []
    current_total, prev_total, current_values, current_labels = update_current_total_gain(race_parties)
    for party in race_parties:
        vote_totals1 = race_parties[str(party)]
        vval1 = vote_totals1[len(vote_totals1) - 1]
        vval2 = vote_totals1[len(vote_totals1) - 2]
        gain = int(vval1) - int(vval2)
        propgain = int(vval1) / sum(current_total)
        formatted_propgain = round((propgain * 100), 3)
        prevp = int(vval2) / sum(prev_total)
        previous_polling = round((prevp * 100), 3)
        party_name = str(party)
        polling_change = round((float(formatted_propgain) - float(previous_polling)), 3)
        data.append([vval2, vval1, gain, formatted_propgain, previous_polling, polling_change])
        row_labels.append(party_name)

    print(row_labels)
    return data, row_labels, current_values, current_labels


def load_race_data(data_path):
    race_data = []  # the data for the race
    with open(data_path) as f:
        data = json.load(f)
    for item in data.items():
        race_data.append(item)
    return race_data


def generate_graph(columns, data, outputpath):

    f = Figure(figsize=(9, 1.9))

    stats = f.add_subplot()
    stats.table(cellText=data, colLabels=columns, rowLabels=row_labels, loc='center')
    stats.xaxis.set_visible(False)
    stats.yaxis.set_visible(False)
    stats.set_title("General Statistics")

def update_states(state):
    """This function loads the json settings file, adds a state, and dumps the file back to json."""
    with open('data/settings/settings.json', "r") as f:
        settings_json = json.load(f)
    states_to_load = settings_json["states"]
    states_to_load.append(state)
    settings_json["states"] = states_to_load
    with open('data/settings/settings.json', "w+") as f:
        json.dump(settings_json, f)

def remove_states(state):
    """This function loads the json settings file, removes a state, and dumps the file back to json."""
    with open('data/settings/settings.json', "r") as f:
        settings_json = json.load(f)
    states_to_load = settings_json["states"]
    states_to_load.remove(state)
    settings_json["states"] = states_to_load
    with open('data/settings/settings.json', "w+") as f:
        json.dump(settings_json, f)

class RaceTracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ This class contains commands and functions related to the bot's ability to track races, using data (formatted in json) that comes from
        updates.py and is stored in /data/results
        """

    pb = commands.Bot(command_prefix=['!', '.'])

    @pb.command(pass_context=True, aliases=["state"])
    @commands.has_any_role("Strategist", "Bot Master", "Verified", "Politburo Member", "Internal Affairs Chair")
    async def states(self, ctx):
        """Retrieves a list of states being updated every 10 minutes, along with the race being scraped."""
        with open('data/settings/settings.json', "r") as f:
            settings = json.load(f)
        states_to_load = settings["states"]
        race = settings["race"]
        embed = discord.Embed(
            title="States Being Watched",
            description="These states are set to update every 10 minutes",
            color=0x00bfff
        )
        for state in states_to_load:
            embed.add_field(name=f'**{state}**',
                            value=f'{race}',
                            inline=False)

        await ctx.send(embed=embed)

    @pb.command(pass_context=True, aliases=["add"])
    @commands.has_any_role("Strategist", "Bot Master", "Verified", "Politburo Member", "Internal Affairs Chair")
    async def addstate(self, ctx, state):
        """Adds a state to the list of states being scraped, takes 20 full minutes or two ten minute update cycles to show results. Whichever comes sooner. """
        update_states(state)
        embed = discord.Embed(title="Added state!", description=f"Succesfully added the state {state}!", color=0x00bfff)
        await ctx.send(embed=embed)

    @pb.command(pass_context=True, aliases=["rem"])
    @commands.has_any_role("Strategist", "Bot Master", "Verified", "Politburo Member", "Internal Affairs Chair")
    async def removestate(self, ctx, state):
        """Removes a state from the list of states being scraped. Data will remain available & accessible through updateraces until overwritten or manually deleted."""
        remove_states(state)
        embed = discord.Embed(title="Remove state!", description=f"Succesfully removed the state {state}!", color=0x00bfff)
        await ctx.send(embed=embed)

    @pb.command(pass_context=True,aliases=["ur"])
    @commands.has_any_role("Strategist", "Bot Master", "Verified", "Politburo Member", "Internal Affairs Chair")
    async def updaterace(self, ctx, state):
        """This command checks the status of a state's polling. The state must be in the tracking list and needs
         two CORRECTLY SCRAPED updates. If they are not displaying properly or display no change, that update was likely
         lost due to lag.
         """
        try:
            data_path = f'data/results/{state}.json'
            loaded_data = load_race_data(data_path)
            race_parties, race_times, race_votes = parse_race_data(loaded_data)
            print(str(race_parties))
            race_data, row_labels, current_polling, current_labels = update_stats(race_parties)

            n = 0
            update_time = time.ctime(os.path.getmtime(data_path))
            embed = discord.Embed(
                title=f"{state}",
                description=f"You've queried for information on {state}, last updated {update_time}!",
                color=0x00bfff
            )
            f = plt.Figure(figsize=(5, 2))
            current = f.add_subplot(111)
            current.pie(current_polling, labels=current_labels, autopct='%1.1f%%')
            current.set_title("Last Update")
            f.savefig('currentgraph.png')
            for row in row_labels:
                cd = race_data[n] # candidate data
                embed.add_field(name=f'**{row}**',
                                value=f'> **Trending To**: {current_polling[n]}%\n'
                                      f'> **Actual Poll Change**: {cd[5]}\n'
                                      f'> % This Update: {cd[3]}\n'
                                      f'> % Last Update: {cd[4]}\n'
                                      f'> Votes Gained: {cd[2]}\n'

                                     ,
                                inline=False)
                n += 1
            chart = discord.File("currentgraph.png", filename="currentgraph.png")
            await ctx.send(embed=embed)
            await ctx.send(file=chart)
        except Exception as e:
            print(f"An error occurred {e}!")
            raise e


def setup(pb):
    pb.add_cog(RaceTracker(pb))
