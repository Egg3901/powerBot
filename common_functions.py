import requests
import lxml
from bs4 import BeautifulSoup
import discord
import os
from tinydb import TinyDB, Query, where
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

power_url = "https://oppressive.games/power/"
USER = os.getenv('USER')
PASS = os.getenv('PASS')
login_data = {'username': f'{USER}', 'password': f'{PASS}', "login": "true"}
db = TinyDB('db.json')
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))


def load_settings():
    with open('data/settings/settings.json', "r") as f:
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


def index_state(state, race):
    """Categorizes states by whether they have a governor/legislature or not"""
    if state in ["USA", "AK", "AL", "NM", "HI", "NH", "ME", "WY", "MT"]:
        index_search = {
            "s1": 4,
            "s2": 5
        }

    elif state in ["China", "Zhongnan", "Huabei"]:
        index_search = {
            "legislature": 3
        }
    else:
        index_search = {
            "s1": 6,
            "s2": 7,
            "gov": 9
        }
    index = index_search[race]
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
