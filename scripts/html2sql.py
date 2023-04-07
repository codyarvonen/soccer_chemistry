import pickle
import sqlite3
from tqdm import tqdm
from bs4 import BeautifulSoup

class Player:
    def __init__(self, name: str, id: int, link: str):
        self.name = name
        self.id = id
        self.link = link

class LineupData:
    def __init__(self, player: Player, match: int, team: int, type: str, sub_time: int):
        self.player = player
        self.match = match
        self.team = team
        self.type = type
        self.sub_time = sub_time

    def __str__(self) -> str:
        return '(' + self.type + ') ' + self.player.name
    
    def table_entry(self):
        return (self.player.name, self.match, self.team, self.type, self.sub_time)



with open('espn-html-pages.pkl', 'rb') as f:

    conn = sqlite3.connect('../../lineups.db')
    # conn.execute('PRAGMA cache_size = 100000')
    cursor = conn.cursor()
    conn.isolation_level = None

    no_lineups = 0
    errors = 0

    pages = pickle.load(f)

    num_pages = 0

    for page in tqdm(pages, total=len(pages)):

        num_pages += 1

        if page == '***No Lineups***':
            no_lineups += 1
        elif page == '*403*' or page == '*4XX*':
            errors += 1
        else:
            match_id = int(page[0])
            match_link = f'https://www.espn.com/soccer/match/_/gameId/{match_id}'
            soup = BeautifulSoup(page[1], "html.parser")
            lineups_data = soup.find(id="gamepackage-game-lineups")
            date_data = soup.find(id="gamepackage-game-information")
            teams_data = soup.find(id="custom-nav")

            if len(lineups_data) > 0:
            
                home_team, away_team = teams_data.find_all('span', class_='long-name')
                home_team, away_team = home_team.text, away_team.text

                home_team_id, away_team_id = teams_data.find_all('div', class_='team-container')

                home_team_href = home_team_id.find('a', href=True)
                away_team_href = away_team_id.find('a', href=True)

                if home_team_href is not None and away_team_href is not None:

                    home_team_link, away_team_link = home_team_href['href'], away_team_href['href']
                    home_team_id, away_team_id = int(home_team_link.split('/')[5]), int(away_team_link.split('/')[5])

                    home_goal, away_goal = teams_data.find_all('div', class_='score-container')

                    if home_goal.text.strip().isdigit() and away_goal.text.strip().isdigit():
                        home_goal, away_goal = int(home_goal.text.strip()), int(away_goal.text.strip())


                        date = date_data.select('span[data-date]')[0]['data-date'].split('T')[0]

                        # table_accordion
                        tables = lineups_data.find_all('table', {'data-behavior': 'table_accordion'})

                        if len(tables) == 2:

                            home_lineups = tables[0].find_all('tbody')
                            away_lineups = tables[1].find_all('tbody')

                            if len(home_lineups) > 1 and len(away_lineups) > 1:

                                home_lineup = home_lineups[0]
                                away_lineup = away_lineups[0]

                                home_bench = home_lineups[1]
                                away_bench = away_lineups[1]

                                home_positions = home_lineup.find_all('td')
                                away_positions = away_lineup.find_all('td')

                                home_positions_bench = home_bench.find_all('td')
                                away_positions_bench = away_bench.find_all('td')

                                home_players = []
                                away_players = []

                                for position in home_positions:
                                    players = position.find_all('div', class_='accordion-item')
                                    if len(players) == 1:
                                        href = players[0].find('a', href=True)                
                                        starter = Player(href.text.strip(), int(players[0]['data-id']), href['href'])
                                        player = LineupData(starter, match_id, home_team_id, 'Starter', None)
                                        home_players.append(player)
                                    elif len(players) == 2:
                                        href = players[0].find('a', href=True)
                                        starter = Player(href.text.strip(), int(players[0]['data-id']), href['href'])
                                        href2 = players[1].find('a', href=True)
                                        sub = Player(href2.text.strip(), int(players[1]['data-id']), href2['href'])

                                        sub_time = int(players[1].find('span', class_='icon-font-before icon-soccer-substitution-before').find('span', class_='detail').text.split('\'')[0])
                                        player1 = LineupData(starter, match_id, home_team_id, 'Starter', sub_time)
                                        player2 = LineupData(sub, match_id, home_team_id, 'Sub', sub_time)

                                        home_players.append(player1)
                                        home_players.append(player2)
                                
                                for position in away_positions:
                                    players = position.find_all('div', class_='accordion-item')
                                    if len(players) == 1:
                                        href = players[0].find('a', href=True)                
                                        starter = Player(href.text.strip(), int(players[0]['data-id']), href['href'])
                                        player = LineupData(starter, match_id, away_team_id, 'Starter', None)
                                        away_players.append(player)
                                    elif len(players) == 2:
                                        href = players[0].find('a', href=True)
                                        starter = Player(href.text.strip(), int(players[0]['data-id']), href['href'])
                                        href2 = players[1].find('a', href=True)
                                        sub = Player(href2.text.strip(), int(players[1]['data-id']), href2['href'])

                                        sub_time = int(players[1].find('span', class_='icon-font-before icon-soccer-substitution-before').find('span', class_='detail').text.split('\'')[0])
                                        player1 = LineupData(starter, match_id, away_team_id, 'Starter', sub_time)
                                        player2 = LineupData(sub, match_id, away_team_id, 'Sub', sub_time)
                                        
                                        away_players.append(player1)
                                        away_players.append(player2)
                                

                                for bench in home_positions_bench:
                                    players = bench.find_all('div', class_='accordion-item')
                                    if len(players) == 1:
                                        href = players[0].find('a', href=True)                
                                        starter = Player(href.text.strip(), int(players[0]['data-id']), href['href'])
                                        player = LineupData(starter, match_id, home_team_id, 'Bench', None)
                                        home_players.append(player)
                                
                                for bench in away_positions_bench:
                                    players = bench.find_all('div', class_='accordion-item')
                                    if len(players) == 1:
                                        href = players[0].find('a', href=True)                
                                        starter = Player(href.text.strip(), int(players[0]['data-id']), href['href'])
                                        player = LineupData(starter, match_id, away_team_id, 'Bench', None)
                                        away_players.append(player)


                                # MAKE DB ENTRIES

                                # Check if teams are already in the table
                            
                                team_query = 'SELECT * FROM teams WHERE team_id = ?'
                                cursor.execute(team_query, (home_team_id,))
                                home_team_entry = cursor.fetchone()
                                cursor.execute(team_query, (away_team_id,))
                                away_team_entry = cursor.fetchone()

                                add_teams = False
                                team_entry_vals = []
                                if home_team_entry is None:
                                    team_entry_vals.append((home_team_id, home_team, home_team_link))
                                    add_teams = True
                                if away_team_entry is None:
                                    team_entry_vals.append((away_team_id, away_team, away_team_link))
                                    add_teams = True

                                if add_teams:
                                    cursor.execute('BEGIN')
                                    insert_team = 'INSERT INTO teams (team_id, team_name, team_link) VALUES (?, ?, ?)'
                                    cursor.executemany(insert_team, team_entry_vals)
                                    cursor.execute('COMMIT')
                                    add_teams = False


                                # Check if each player is already in the table

                                all_players = home_players + away_players

                                player_query = 'SELECT * FROM players WHERE player_id = ?'
                                player_entry_vals = []
                                add_players = False
                                for player in all_players:
                                    cursor.execute(player_query, (player.player.id,))
                                    player_entry = cursor.fetchone()
                                    if player_entry is None:
                                        player_entry_vals.append((player.player.id, player.player.name, player.player.link))
                                        add_players = True

                                if add_players:
                                    cursor.execute('BEGIN')
                                    insert_player = 'INSERT INTO players (player_id, player_name, player_link) VALUES (?, ?, ?)'
                                    cursor.executemany(insert_player, player_entry_vals)
                                    cursor.execute('COMMIT')
                                    add_players = False


                                # Insert match data

                                insert_match = 'INSERT INTO matches (match_id, match_link, date, home_team_id, away_team_id, home_team_goal, away_team_goal) VALUES (?, ?, ?, ?, ?, ?, ?)'
                                match_data = (match_id, match_link, date, home_team_id, away_team_id, home_goal, away_goal)
                                cursor.execute(insert_match, match_data)
                                conn.commit()


                                # Insert all lineups

                                cursor.execute('BEGIN')
                                lineup_query = 'INSERT INTO lineups (player_id, match_id, team_id, player_type, sub_time) VALUES (?, ?, ?, ?, ?)'
                                
                                lineups_entries = []
                                for player in home_players:
                                    lineups_entries.append(player.table_entry())
                                for player in away_players:
                                    lineups_entries.append(player.table_entry())

                                cursor.executemany(lineup_query, lineups_entries)
                                cursor.execute('COMMIT')


    cursor.close()
    conn.close()

    print(f'Pages w/o lineups: {no_lineups}')
    print(f'Pages w/ errors: {errors}')