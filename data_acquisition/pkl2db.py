import time
import sqlite3
import pickle
from tqdm import tqdm
from bs4 import BeautifulSoup

# THIS DOESN'T TAKE RED CARDS INTO ACCOUNT

connection = sqlite3.connect('lineups.db')
cursor = connection.cursor()

start_time = time.perf_counter()

with open('pages62.pkl', 'rb') as f:
    pages = pickle.load(f)

    for page in tqdm(pages):
        if page.status_code < 300:
            soup = BeautifulSoup(page.text, "html.parser")
            lineups_data = soup.find(id="gamepackage-game-lineups")
            if len(lineups_data) > 0:
                url = page.url
                game_id = int(url.split('/')[7])
                teams = soup.find_all("div", class_ = "team-info-wrapper")
                scores = soup.find_all("div", class_ = "score-container")

                home_score = scores[0].text.strip()
                away_score = scores[1].text.strip()
                if home_score == '':
                    home_score = None
                else:
                    home_score = int(scores[0].text.strip())
                if away_score == '':
                    away_score = None
                else:
                    away_score = int(scores[1].text.strip())

                a_home = teams[0].find('a', href=True)
                a_away = teams[1].find('a', href=True)

                if a_home is not None and a_away is not None:
                    home_num = a_home['data-clubhouse-uid']
                    away_num = a_away['data-clubhouse-uid']

                    home_id = int(home_num.split(':')[2])
                    home_url = 'http://www.espn.com' + a_home['href']
                    home_name = a_home.find('span', class_ = 'short-name').text
                    
                    away_id = int(away_num.split(':')[2])
                    away_url = 'http://www.espn.com' + a_away['href']
                    away_name = a_away.find('span', class_ = 'short-name').text

                    date = ''
                    dates = soup.find(id="gamepackage-game-information").find_all('span')
                    for d in dates:
                        if 'data-date' in d.attrs:
                            date = d.attrs['data-date'].split('T')[0]

                    
                    lineups = lineups_data.find_all("div", class_="content")

                    player_tables = []
                    for lineup in lineups:
                        player_tables.append(lineup.find('table').find_all('tbody'))
                    
                    cursor.execute("""INSERT INTO matches (match_id, match_link, date, home_team_id, away_team_id, home_team_goal, away_team_goal) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?)""", (game_id, url, date, home_id, away_id, home_score, away_score))

                    cursor.execute("""INSERT INTO teams (team_id, team_name, team_link) SELECT ?, ?, ?
                                        WHERE NOT EXISTS (SELECT 1 FROM teams WHERE team_id = ? and team_name = ? and team_link = ?)""", 
                                        (home_id, home_name, home_url) * 2)

                    cursor.execute("""INSERT INTO teams (team_id, team_name, team_link) SELECT ?, ?, ?
                                        WHERE NOT EXISTS (SELECT 1 FROM teams WHERE team_id = ? and team_name = ? and team_link = ?)""", 
                                        (away_id, away_name, away_url) * 2)

                    for i, table in enumerate(player_tables):
                        for j, body in enumerate(table):
                            for player_row in body.find_all('tr'):
                                players = player_row.find_all('div', class_ = 'accordion-item')
                                for s, player in enumerate(players):
                                    a = player.find('a', href=True)
                                    type = ''
                                    if j == 0 and s == 0:
                                        type = 'Starter'
                                    elif j == 0:
                                        type = 'Sub'
                                    else:
                                        type = 'Bench'
                                    
                                    player_id = 0
                                    if player['data-id'].isdigit():
                                        player_id = int(player['data-id'])
                                    else:
                                        break
                                    player_name = a.text.strip()
                                    player_link = a['href']

                                    sub_time = None
                                    if len(players) > 1:
                                        p = players[1].find('span', class_ = 'detail')
                                        if p is not None:
                                            sub_time = int(p.text.split('\'')[0])

                                    team_id = 0
                                    if i == 0:
                                        team_id = home_id
                                    else:
                                        team_id = away_id
                                    


                                    # cursor.execute("""INSERT INTO players (player_id, player_name, player_link) SELECT ?, ?, ?
                                    #                     WHERE NOT EXISTS (SELECT 1 FROM players WHERE player_id = ? and player_name = ? and player_link = ?)""", 
                                    #                     (player_id, player_name, player_link) * 2)
                                    cursor.execute("""INSERT INTO players (player_id, player_name, player_link) SELECT ?, ?, ?
                                                        WHERE NOT EXISTS (SELECT 1 FROM players WHERE player_id = ?)""", 
                                                        (player_id, player_name, player_link, player_id))

                                    cursor.execute("""INSERT INTO lineups (player_id, match_id, team_id, player_type, sub_time) VALUES (?, ?, ?, ?, ?)""",
                                                        (player_id, game_id, team_id, type, sub_time))


end_time = time.perf_counter()

print("Elapsed time: {}".format(end_time - start_time))

connection.commit()
connection.close()

