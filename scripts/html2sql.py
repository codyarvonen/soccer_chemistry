import pickle
from bs4 import BeautifulSoup

with open('pages-test.pkl', 'rb') as f:
    pages = pickle.load(f)
    # print(len(pages))
    soup = BeautifulSoup(pages[0].text, "html.parser")
    lineups_data = soup.find(id="gamepackage-game-lineups")
    date_data = soup.find(id="gamepackage-game-information")
    teams_data = soup.find(id="custom-nav")

    if len(lineups_data) > 0:
        print("Retreiving lineups for game")
    
        home_team, away_team = teams_data.find_all('span', class_='long-name')
        home_team, away_team = home_team.text, away_team.text

        home_team_id, away_team_id = teams_data.find_all('div', class_='team-container')
        home_team_id, away_team_id = int(home_team_id.find('a', href=True)['href'].split('/')[5]), int(away_team_id.find('a', href=True)['href'].split('/')[5])

        home_goal, away_goal = teams_data.find_all('div', class_='score-container')
        home_goal, away_goal = int(home_goal.text.strip()), int(away_goal.text.strip())


        date = date_data.select('span[data-date]')[0]['data-date'].split('T')[0]

        print(home_goal, away_goal)
