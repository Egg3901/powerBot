import lxml
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query, where
from commonFunctions import load_settings, power_url, session, msgs, date_time, db, scrape


def parse_election_results(soup, index):
    election_table = soup.findAll("div", {"class": "card-body"})[index]
    election_table_rows = election_table.findAll("tr")
    senate_1_results_votes = []
    rem_time = election_table.find_all("font")
    rem_time = rem_time[0].text
    rem_time_format = rem_time[:-6][12:]
    update_results = {rem_time_format: []}
    for row in election_table_rows:
        if "Votes" in str(row):
            row_data = row.find_all("td")
            votes = row_data[2].text
            name = row_data[0].text
            party = row_data[1].text
            vote_list = votes.split()
            percent = str(vote_list[0]).replace(",", "")
            voters = vote_list[1].replace("%", "")
            vote_data = [name, party, voters, percent]
            senate_1_results_votes.append(vote_data)
            update_results[rem_time_format].append(
                {"party": party, "name": name, "voters": voters, "percent": percent})
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
    settings = load_settings()
    states_to_update = settings["states"]
    race = settings["race"]
    for state in states_to_update:
        index = index_state(state, race) # indexes the state and determines which table to search
        try:
            soup = scrape(f'{power_url}/state.php?state={state}')
            update_results = parse_election_results(soup, index)
        except Exception as e:
            msgs(f"An error occurred!",f"Error parsing information for {state} - {race}, the details of the exception:"
                                       f"{e}")
            break
        election = Query()
        table_name = f"{state}_{race}"
        matching_tables = db.search(election.name == table_name)  # searches for the table in the database
        if len(matching_tables) < 1:
            """The table does not exist"""
            election_table = db.table(table_name)
            election_blank_update = {}
            election_table.update({'election_update_one': update_results, 'election_update_two': election_blank_update})
        else:
            """There is existing data on this race!"""
            election_table = db.table(table_name)
            previous_update = election_table.table_name.election_update_one  # selects the previous update
            election_table.update({'election_update_one': update_results, 'election_update_two': previous_update})



