import sys
import pickle
import sqlite3
import numpy as np
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt

from total_minutes import get_total

# DOES NOT TAKE INTO ACCOUNT RED CARDS OR 120 MINUTE GAMES

# def get_minutes_played(result):
#     if result[3] == "Starter" and result[6] == "Starter":
#         if result[4] is None and result[7] is None:
#             return 90
#         elif result[4] is None or result[7] is None:
#             return result[4] if result[7] is None else result[7]
#         else:
#             return result[4] if result[4] < result[7] else result[7]
#     elif result[3] == "Starter" or result[6] == "Starter":
#         if result[3] == "Starter":
#             if result[4] is None:
#                 w = 90 - result[7]
#             else:
#                 w = result[4] - result[7]
#             if w < 0:
#                 return 0
#             return w
#         else:
#             if result[7] is None:
#                 w = 90 - result[4]
#             else:
#                 w = result[7] - result[4]
#             if w < 0:
#                 return 0
#             return w
#     else:
#         return 90 - result[4] if result[4] > result[7] else 90 - result[7]

def get_minutes_played(result):
    if result[1] == "Starter" and result[4] == "Starter":
        if result[2] is None and result[5] is None:
            return 90
        elif result[2] is None or result[5] is None:
            return result[2] if result[5] is None else result[5]
        else:
            return result[2] if result[2] < result[5] else result[5]
    elif result[1] == "Starter" or result[4] == "Starter":
        if result[1] == "Starter":
            if result[2] is None:
                if result[5] is None:
                    return 0
                w = 90 - result[5]
            else:
                w = result[2] - result[5]
            if w < 0:
                return 0
            return w
        else:
            if result[5] is None:
                if result[2] is None:
                    return 0
                # print(result[0], result[3])
                w = 90 - result[2]
            else:
                w = result[5] - result[2]
            if w < 0:
                return 0
            return w
    else:
        return 90 - result[2] if result[2] > result[5] else 90 - result[5]


if __name__ == "__main__":

    player_id = int(sys.argv[1])

    if sys.argv[2] == "create":

        connection = sqlite3.connect('lineups.db')
        cursor = connection.cursor()

        G = nx.Graph()

        player_name = cursor.execute("SELECT DISTINCT player_name FROM players WHERE player_id = ?", (player_id,))
        G.add_node(player_id)
        G.nodes[player_id]["name"] = player_name.fetchall()[0][0]
        # print(G.nodes[player_id])

        print("Getting data from database")
        results = cursor.execute("""SELECT DISTINCT a.match_id AS 'matchID',
                                                    a.team_id AS 'teamID',
                                                    a.player_id AS 'player1',
                                                    a.player_type AS 'playerType1',
                                                    a.sub_time AS 'subTime1',
                                                    b.player_id AS 'player2',
                                                    b.player_type AS 'playerType2',
                                                    b.sub_time AS 'subTime2',
                                                    d.player_name AS 'name'
                                    FROM lineups a
                                    INNER JOIN lineups b ON a.match_id = b.match_id AND a.team_id = b.team_id
                                    INNER JOIN players d ON d.player_id = b.player_id
                                    WHERE a.player_id = ? AND b.player_id != ? AND a.player_type != 'Bench' AND b.player_type != 'Bench';""",
                                    (player_id, player_id))

        print("Populating graph")
       
        for result in tqdm(results):
            w = get_minutes_played(result)
            if G.has_edge(result[2], result[5]):
                G.edges[result[2], result[5]]["weight"] += w
            else:
                G.add_edge(result[2], result[5], weight=w)
            G.nodes[result[5]]["name"] = result[8]
            # G.nodes[result[2]]["weight"] = get_total(connection, result[2])[1]

        # print(G.nodes.data("name"))

        for node in tqdm(list(G.nodes)):
            G.nodes[node]["weight"] = get_total(connection, node)[1]

        with open('player{}.pkl'.format(player_id), 'wb') as f:
            pickle.dump(G, f)

        connection.commit()
        # print("Getting node sizes")
        # node_sizes = [get_total(connection, node)[1] for node in list(G.nodes)]
        # print("Getting weight sizes")
        e_weights = list(zip(*list(G.edges.data("weight"))))[2]
        n_weights = list(zip(*list(G.nodes.data("weight"))))[1]
        pos = nx.random_layout(G)

        connection.close()

        

        nx.draw(G, pos, with_labels=True, labels=dict(G.nodes.data("name")), node_size=[w * 2000/ max(n_weights) for w in n_weights], width=[w * 10 / max(e_weights) for w in e_weights], node_color="skyblue", node_shape="o")
        plt.show()


        # print(list(G.nodes))
        # print(list(G.edges))

        # ws = np.array(weights)

        # for node_index in np.flip(np.argsort(ws)):
        #     print(list(G.nodes)[node_index+1], G.edges[45843, list(G.nodes)[node_index+1]])

    elif sys.argv[2] == "load":
        with open('player{}.pkl'.format(player_id), 'rb') as f:
            G = pickle.load(f)
            e_weights = list(zip(*list(G.edges.data("weight"))))[2]
            n_weights = list(zip(*list(G.nodes.data("weight"))))[1]
            pos = nx.random_layout(G)
            with open('player{}.pkl'.format(player_id), 'wb') as f:
                pickle.dump(G, f)

            nx.draw(G, pos, with_labels=True, labels=dict(G.nodes.data("name")), node_size=[w * 2000/ max(n_weights) for w in n_weights], width=[w * 10 / max(e_weights) for w in e_weights], node_color="skyblue", node_shape="o")
            plt.show()
