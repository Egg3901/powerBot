import json
from datetime import datetime
import lxml
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv


load_dotenv()

USER = os.getenv('USER')
PASS = os.getenv('PASS')

login_data = {'username': f'{USER}', 'password': f'{PASS}', "login":"true"}
now = datetime.now()


def update_population():
    with open('data/settings/settings.json', "r") as f:
        settings = json.load(f)
    states_to_update = settings["states"]
    race = settings["race"]
    print(f"Updating {states_to_update}")
    url = "https://www.oppressive.games/power/"
    session = requests.Session()

    try:
        print(str(login_data))
        session.post(f'{url}/login.php', data=login_data)
    except Exception as e:
        print('error during login')
        print(str(e))
    for state in states_to_update:
        if state in ["AK", "AL", "NM", "HI", "NH", "ME"]:
            index_search = {
                "s1": 4,
                "s2": 5

            }
        else:
            index_search = {
                "s1": 6,
                "s2": 7,
                "gov": 9
            }
        index = index_search[race]
        output_json_path = (f'data/results/{state}{race}.json')

        try:
            sp_res = session.get(f'{url}/state.php?state={state}', data=login_data)
            soup = BeautifulSoup(sp_res.text, 'lxml')
            election_table = soup.findAll("div", {"class": "card-body"})[index]

            election_table_rows = election_table.findAll("tr")
            senate_1_results_votes = []
            rem_time = election_table.find_all("font")
            rt = rem_time[0].text
            rtformatted = rt[:-6][12:]
            json_results = {rtformatted: []}
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
                    json_results[rtformatted].append(
                        {"party": party, "name": name, "voters": voters, "percent": percent})

        except Exception as e:
            print(str(e))

        try:
            with open(output_json_path) as f:
                data = json.load(f)

        except Exception as e:
            print(f"Creating {output_json_path}!")
            with open(output_json_path, "a+") as f:
                f.write(json.dumps({}))
                f.close()

        with open(output_json_path) as f:
            data = json.load(f)


        with open(output_json_path, 'w') as f:
            data.update(json_results)
            json.dump(data, f)
        print(f'{state} update!')


