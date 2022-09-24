import sqlite3
import pickle
import sys
import numpy as np
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
from itertools import combinations

from create_player_graph import get_minutes_played

# DOES NOT TAKE INTO ACCOUNT RED CARDS OR 120 MINUTE GAMES


# Fetches the match data from the database and stores it in a pickle file
def get_match_stats(connection:sqlite3.Connection, match_id, dir_name):
    cursor = connection.cursor()
    players = {}

    results = cursor.execute("""SELECT DISTINCT a.player_id, a.team_id, b.date, b.home_team_id, b.away_team_id, b.home_team_goal, b.away_team_goal
                                    FROM lineups a
                                    INNER JOIN matches b ON a.match_id = b.match_id
                                    WHERE a.match_id = ? AND a.player_type = 'Starter';""", (match_id,))
    results = results.fetchall()

    for result in results:
        if result[1] in players:
            players[result[1]].append(result[0])
        else:
            players[result[1]] = [result[0]]

    date = results[0][2]
    home_team_id = results[0][3]
    away_team_id = results[0][4]
    home_goal = results[0][5]
    away_goal = results[0][6]

    G = nx.Graph(date=date, home_team_id=home_team_id, away_team_id=away_team_id, home_goal=home_goal, away_goal=away_goal)

    for team in players:
        for player_a, player_b in list(combinations(players[team], 2)):
            if player_a != player_b:
                results = cursor.execute("""SELECT DISTINCT a.player_id AS 'player1',
                                                            a.player_type AS 'playerType1',
                                                            a.sub_time AS 'subTime1',
                                                            b.player_id AS 'player2',
                                                            b.player_type AS 'playerType2',
                                                            b.sub_time AS 'subTime2'
                                            FROM lineups a 
                                            INNER JOIN lineups b ON a.match_id = b.match_id AND a.team_id = b.team_id 
                                            INNER JOIN matches c ON c.match_id = a.match_id AND c.match_id = b.match_id
                                            WHERE c.date < ? AND a.player_id = ? AND b.player_id = ? AND a.player_type != 'Bench' AND b.player_type != 'Bench';""", 
                                            (date, player_a, player_b))
                for result in results:
                    w = get_minutes_played(result)
                    if G.has_edge(result[0], result[3]):
                        G.edges[result[0], result[3]]["weight"] += w
                    else:
                        G.add_edge(result[0], result[3], weight=w, team=team)
    
    with open('{}/match{}.pkl'.format(dir_name, match_id), 'wb') as f:
        pickle.dump(G, f)

    connection.commit()

    connection.close()

def main():
    connection = sqlite3.connect('lineups.db')

    mem = sqlite3.connect(':memory:')
    connection.backup(mem)
    cursor = connection.cursor()

    # positions433 = [[0.25, 0.05], [0.2, 0.1], [0.3, 0.1], [0.1, 0.15], [0.4, 0.15], [0.25, 0.25], [0.15, 0.2], [0.35, 0.2], [0.25, 0.4], [0.15, 0.35], [0.35, 0.35]]
    # positions442 = [[0.25, 0.05], [0.2, 0.1], [0.3, 0.1], [0.1, 0.15], [0.4, 0.15], [0.2, 0.25], [0.3, 0.25], [0.1, 0.3], [0.4, 0.3], [0.2, 0.4], [0.3, 0.4]]
    # positions4312 = [[0.25, 0.05], [0.2, 0.1], [0.3, 0.1], [0.1, 0.15], [0.4, 0.15], [0.25, 0.25], [0.15, 0.3], [0.35, 0.3], [0.25, 0.35], [0.2, 0.5], [0.3, 0.5]]
    # positions4213 = [[0.25, 0.05], [0.2, 0.1], [0.3, 0.1], [0.1, 0.15], [0.4, 0.15], [0.25, 0.35], [0.2, 0.2], [0.3, 0.2], [0.25, 0.45], [0.15, 0.3], [0.35, 0.3]]
    # positions4141 = [[0.25, 0.05], [0.2, 0.1], [0.3, 0.1], [0.25, 0.2], [0.1, 0.15], [0.4, 0.15], [0.2, 0.275], [0.3, 0.274], [0.1, 0.325], [0.4, 0.325], [0.25, 0.4]]
    # positions3142 = [[0.25, 0.05], [0.25, 0.125], [0.15, 0.15], [0.35, 0.15], [0.25, 0.2], [0.2, 0.3], [0.3, 0.3], [0.1, 0.25], [0.4, 0.25], [0.2, 0.4], [0.3, 0.4]]
    # positions4231 = [[0.25, 0.05], [0.2, 0.1], [0.3, 0.1], [0.1, 0.15], [0.4, 0.15], [0.25, 0.3], [0.2, 0.2], [0.3, 0.2], [0.25, 0.4], [0.15, 0.35], [0.35, 0.35]]
    
    # positions = [positions433, positions4231]

    # for i in range(len(positions[1])):
    #     positions[1][i][0] += 0.5

    # match_id = 372838
    match_id = sys.argv[1]
    
    if sys.argv[2] == "create":

        players = {}

        print("Getting data from database")

        results = cursor.execute("""SELECT DISTINCT a.player_id, a.team_id, b.date, b.home_team_id, b.away_team_id, b.home_team_goal, b.away_team_goal
                                    FROM lineups a
                                    INNER JOIN matches b ON a.match_id = b.match_id
                                    WHERE a.match_id = ? AND a.player_type = 'Starter';""", (match_id,))
        
        results = results.fetchall()

        for result in results:
            if result[1] in players:
                players[result[1]].append(result[0])
            else:
                players[result[1]] = [result[0]]

        date = results[0][2]
        home_team_id = results[0][3]
        away_team_id = results[0][4]
        home_goal = results[0][5]
        away_goal = results[0][6]

        # print(players)

        # results = cursor.execute("""SELECT DISTINCT date
        #                             FROM matches 
        #                             WHERE match_id = ?;""", (match_id,))

        # date = results.fetchall()[0][0]

        # print(date)

        G = nx.Graph(date=date, home_team_id=home_team_id, away_team_id=away_team_id, home_goal=home_goal, away_goal=away_goal)

        for team in players:
            for player_a, player_b in tqdm(list(combinations(players[team], 2))):
                if player_a != player_b:
                    print("SQLite")
                    results = cursor.execute("""SELECT DISTINCT a.player_id AS 'player1',
                                                                a.player_type AS 'playerType1',
                                                                a.sub_time AS 'subTime1',
                                                                b.player_id AS 'player2',
                                                                b.player_type AS 'playerType2',
                                                                b.sub_time AS 'subTime2'
                                                FROM lineups a 
                                                INNER JOIN lineups b ON a.match_id = b.match_id AND a.team_id = b.team_id 
                                                INNER JOIN matches c ON c.match_id = a.match_id AND c.match_id = b.match_id
                                                WHERE c.date < ? AND a.player_id = ? AND b.player_id = ? AND a.player_type != 'Bench' AND b.player_type != 'Bench';""", 
                                                (date, player_a, player_b))
                    
                    print("DONE")
                    for result in results:
                        w = get_minutes_played(result)
                        if G.has_edge(result[0], result[3]):
                            G.edges[result[0], result[3]]["weight"] += w
                        else:
                            G.add_edge(result[0], result[3], weight=w)
                        # if G.has_edge(result[2], result[5]):
                        #     G.edges[result[2], result[5]]["weight"] += w
                        # else:
                        #     G.add_edge(result[2], result[5], weight=w)
                        # G.nodes[result[2]]["name"] = result[8]
                            
        
        with open('match{}.pkl'.format(match_id), 'wb') as f:
            pickle.dump(G, f)

        connection.commit()

        connection.close()

        # pos = nx.random_layout(G)
        # print("pos: {}".format(pos))
        # nx.draw(G, pos, with_labels=True, node_color="skyblue", node_shape="o")
        # plt.show()

    elif sys.argv[2] == "load":

        with open('match{}.pkl'.format(match_id), 'rb') as f:
            G = pickle.load(f)
            
            # pos = {}
            # for i, node in enumerate(G.nodes):
            #     pos[node] = positions[int(i>=11)][i%11]

            # weights = list(zip(*list(G.edges.data("weight"))))[2]

            # for p in pos.values():
            #     print(p)
            # nx.draw(G, pos, with_labels=True, labels=dict(G.nodes.data("name")), node_size=1000, width=[w * 10 / max(weights) for w in weights], node_color="skyblue", node_shape="o")
            # plt.show()


if __name__ == "__main__":
    main()