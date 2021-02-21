import requests
from bs4 import BeautifulSoup
import discord
import os
from tinydb import TinyDB, Query, where
import json
from datetime import datetime

power_url = "https://oppressive.games/power/"
USER = os.getenv('USER')
PASS = os.getenv('PASS')
login_data = {'username': f'{USER}', 'password': f'{PASS}', "login": "true"}
db = TinyDB('db.json')
session = requests.Session()
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


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


def login_to_power(ld, p_url):
    """Very common function used to login to POWER prior to scraping data"""
    session = requests.session()
    try:
        session.post(f'{p_url}/login.php', data=ld)
    except Exception as e:
        print('error during login')
        print(str(e))

    return session


def scrape(url):
    login_to_power(ld=login_data, p_url=power_url)
    scrape_response = session.get(url)
    soup = BeautifulSoup(scrape_response.text, 'lxml')
    return soup


def msgs(title, message):
    embed = discord.Embed(title=title, description=message, color=0x800020)
    return embed


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

