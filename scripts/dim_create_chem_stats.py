import os
import pickle
import sqlite3
import numpy as np
import networkx as nx

dir = 'dim_WC_2022'

# key = match_id
# value = [(home_id, [list of home weights], home_score), (away_id, [list of away weights], away_score), date]
stats = {}

for match_file in os.listdir(dir):
    if not match_file.startswith('.'):
        match = os.path.join(dir, match_file)
        print(match)
        with open(match, 'rb') as f:
            G = pickle.load(f)

            match_id = int(match.split('h')[1].split('.')[0])

            # connection = sqlite3.connect('lineups.db')
            # cursor = connection.cursor()
            # results = cursor.execute("""SELECT DISTINCT player_id, team_id
            #                             FROM lineups
            #                             WHERE match_id = ? AND player_type = 'Starter';""", (match_id,))

            # results = results.fetchall()

            home_w = []
            away_w = []
            # for edge in list(G.edges):
            #     node = edge[0]
            #     t = (node, int(G.graph['home_team_id']))
            #     if t in results:
            #         home_w.append(G.edges[edge[0], edge[1]]['weight'])
            #     else:
            #         away_w.append(G.edges[edge[0], edge[1]]['weight'])

            for edge in G.edges:
                if G.edges[edge[0], edge[1]]['team'] == int(G.graph['home_team_id']):
                    home_w.append(G.edges[edge[0], edge[1]]['weight'])
                else:
                    away_w.append(G.edges[edge[0], edge[1]]['weight'])

            stats[match_id] = [(int(G.graph['home_team_id']), home_w, int(G.graph['home_goal'])), (int(G.graph['away_team_id']), away_w, int(G.graph['away_goal'])), G.graph['date']]


with open('{}.pkl'.format(dir), 'wb') as f:
    pickle.dump(stats, f)