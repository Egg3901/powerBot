import lxml
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query, where
from common_functions import load_settings, power_url, msgs, date_time, db, scrape, login_data, index_state
import os
from dotenv import load_dotenv

USER = os.getenv('USER')
PASS = os.getenv('PASS')
login_data = {'username': f'{USER}', 'password': f'{PASS}', "login": "true"}


def parse_election_results(soup, index):
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


def index_state(state, race):
    """Categorizes states by whether they have a governor/legislature or not"""
    if state in ["AK", "AL", "NM", "HI", "NH", "ME", "WY", "MT"]:
        index_search = {
            "s1": 4,
            "s2": 5
        }
    elif state in ["Zhongnan", "Huabei"]:
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



def update_population():
    elections_to_update = load_settings()["elections"]
    for election in elections_to_update:
        race = election["race"]
        state = election["region"]
        print(f'Updating {race}, {state}')
        index = index_state(state, race) # indexes the state and determines which table to search
        try:
            soup = scrape(f'{power_url}/state.php?state={state}')
            update_results = parse_election_results(soup, index)
            print(update_results.text)
        except Exception as e:
            msgs(f"An error occurred!",f"Error parsing information for {state} - {race}, the details of the exception:"
                                       f"{e}")
            break
        election = Query()
        table_name = f"{state}_{race}"
        table = db.table(table_name)
        election_table = TinyDB.table(db, table_name)
        print('len gr 1')
        previous_update = table.search(table_name.election_update_one)  # selects the previous update
        election_table.update({'state': state, 'race': race, 'election_update_one': update_results,
                               'election_update_two': previous_update}
                              )


