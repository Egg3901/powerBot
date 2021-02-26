import requests
import lxml
from bs4 import BeautifulSoup
import discord
import os
from tinydb import TinyDB, Query, where
import json
from datetime import datetime
from dotenv import load_dotenv

from common.region_conversion import us_state_abbreviations_list, us_state_names_list, us_state_convert, \
    cn_state_abbreviations_list, cn_state_convert, cn_state_names_list

load_dotenv()

power_url = "https://oppressive.games/power/"
USER = os.getenv('USER')
PASS = os.getenv('PASS')
login_data = {'username': f'{USER}', 'password': f'{PASS}', "login": "true"}
db = TinyDB('db.json')
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")



def load_settings():
    with open('../data/settings/settings.json', "r") as f:
        settings = json.load(f)
    return settings


def register(user_id, power_id):
    print(str(user_id))
    table = db.table('users')
    table.update({'discord_user': user_id, 'power_user': power_id})


def query(user_id):
    user = Query()
    table = db.table('users')
    user_info = table.search(user.discord_user == user_id)
    print(user_info)
    return user_info


def login_to_power(p_url):
    """Very common function used to login to POWER prior to scraping data"""
    session = requests.session()
    ld = {'username': f'{USER}', 'password': f'{PASS}', "login": "true"}
    print(str(ld))
    try:
        session.post(f'{p_url}/login.php', data=ld)
    except Exception as e:
        print('error during login')
        print(str(e))

    return session


def parse_state_parameters(state, race=None):
    us_states = us_state_abbreviations_list()
    us_state_names = us_state_names_list()
    if race is None:
        cn_states = cn_state_abbreviations_list()
        cn_states_names = cn_state_names_list()

        if state.lower() in [x.lower() for x in cn_states_names]:
            """Lowers the state name and checks against list of full state names"""
            index = 3
            return index

        if state.lower() in [x.lower() for x in cn_states]:
            index = 3
            return index

        else:
            index = 0
            return index

    else:
        try:
            us_state_abbrev, abbrev_us_state = us_state_convert()
            state = us_state_abbrev[state]
        except KeyError as e:
            pass

        if state.lower() in [x.lower() for x in us_states]:
            if state in ["AK", "AL", "NM", "HI", "NH", "ME", "WY", "MT"]:
                index_search = {
                    "s1": 4,
                    "s2": 5
                }
                index = index_search[race]
                return index
            else:
                index_search = {
                    "s1": 6,
                    "s2": 7,
                    "gov": 9
                }
                index = index_search[race]
                return index

        else:
            index = 0
            return index





def scrape(url):
    session = login_to_power(p_url=power_url)
    scrape_response = session.get(url)
    soup = BeautifulSoup(scrape_response.text, 'lxml')
    print('url scraped')
    return soup


def msgs(title, message):
    embed = discord.Embed(title=title, description=message, color=0x800020)
    return embed


def parse_profile_information(profile_soup, url):
    s = profile_soup
    try:
        name = s.findAll("h1")[0].text
    except IndexError as e:
        name = "Hillary Rodham Clinton"
    politics = s.find("center").findAll("div", {"class": "col-xl-5"})[1].find("div", {"class": "card"}).findAll("tr")
    info = s.find("center").findAll("div", {"class": "col-xl-5"})[0].findAll("div", {"class": "card"})[0]

    citizenship = politics[1].findAll("td")[1].text
    power = politics[3].findAll("td")[1].text
    campaign_funds = politics[4].findAll("td")[1].text
    home_state_influence = politics[6].findAll("td")[1].text
    reputation = politics[7].findAll("td")[1].text
    party = politics[9].findAll("td")[1].text
    profile_image = f"{power_url}" + info.find("img")['src'].replace(" ", "%20")
    country_link = power_url + politics[1].findAll("td")[1].find("a")['href']

    embed = discord.Embed(title=name, color=0x800020)

    embed.set_author(name=f"{party} Politician")
    embed.set_thumbnail(url=profile_image)
    embed.add_field(name="Citizenship", value=f"[{citizenship}]({country_link})")
    embed.add_field(name="Power", value=power, inline=True)
    embed.add_field(name="Campaign Funds", value=campaign_funds, inline=True)
    embed.add_field(name="State Influence", value=home_state_influence, inline=True)
    embed.add_field(name="Reputation", value=reputation, inline=True)

    return embed

def parse_election_results(soup, index):
    election_table = soup.findAll("div", {"class": "card-body"})[index]
    election_table_rows = election_table.findAll("tr")
    rem_time = election_table.find_all("font")
    rem_time = rem_time[0].text
    rem_time_format = rem_time[:-6][12:]
    update_results = {rem_time_format: {}}
    print(str(update_results))
    for row in election_table_rows:
        if "Votes" in str(row):
            row_data = row.find_all("td")
            votes = row_data[2].text
            name = row_data[0].text
            party = row_data[1].text
            vote_list = votes.split()
            percent = str(vote_list[0]).replace(",", "")
            voters = vote_list[1].replace("%", "")
            update_results[rem_time_format] = {"party": party, "name": name, "voters": voters, "percent": percent}
    print(update_results)
    return update_results

