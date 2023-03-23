import sqlite3
import pickle
import sys
import datetime
import csv
import math
import numpy as np
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
from itertools import combinations

from create_player_graph import get_minutes_played

# DOES NOT TAKE INTO ACCOUNT RED CARDS OR 120 MINUTE GAMES

# Fetches the match data from the database and stores it in a pickle file
def main():
    db_file_name = '../../lineups.db'
    connection = sqlite3.connect(db_file_name)

    today = '2022-08-01'
    players_list_arg = [118577, 158626, 167192, 157557, 242710, 233937, 164826, 228262, 119289, 138341, 96970, 145190, 174466, 285450, 149578, 249299, 228393, 153115, 212185, 277206, 195638, 108223, 164839, 76017, 219713, 45843]
    players_list_aus = [141438, 107530, 115893, 159502, 200414, 276916, 260642, 238368, 207461, 228416, 146833, 218205, 138425, 178071, 227289, 251147, 76917, 235096, 181707, 140994, 139748, 187777, 193008, 156119, 332947, 170754]
    players_list_bel = [134283, 99829, 140079, 111306, 304222, 228421, 125086, 166473, 197163, 314473, 134947, 193849, 193297, 182680, 304799, 174893, 164895, 296319, 174980, 158066, 139437, 156479, 89687, 101390, 276265, 283672]
    players_list_brz = [196876, 176948, 198983, 159047, 228402, 96254, 170369, 199734, 30901, 125514, 258307, 176287, 173666, 218522, 161559, 234715, 199017, 269844, 252107, 132948, 281558, 267804, 231050, 156799, 235017, 217289]
    players_list_cam = [291747, 196163, 215340, 121592, 252474, 246855, 233355, 185683, 242601, 283606, 224064, 260253, 246833, 232545, 277095, 215721, 232623, 286837, 173182, 192055, 147324, 207040, 271170, 102254, 234395, 315640]
    players_list_can = [157292, 257619, 231059, 193452, 238712, 293691, 230626, 249756, 101976, 236890, 270505, 252901, 86524, 237002, 325001, 184221, 87387, 137726, 284769, 172596, 273499, 236721, 116662, 205024, 271879, 225545]
    players_list_crc = [101828, 73247, 228458, 159195, 265898, 186610, 278526, 112866, 201914, 147197, 235122, 132937, 310001, 325358, 183102, 201120, 276951, 137779, 260484, 151369, 141888, 341508, 350718, 166669, 286662, 201917]
    players_list_cra = [187946, 194778, 210092, 276329, 222259, 216579, 123560, 228319, 299910, 148110, 222567, 305552, 237549, 154595, 76762, 306263, 178383, 206378, 189668, 103485, 238929, 139520, 165580, 182097, 207288, 194277]
    players_list_den = [40200, 165424, 249668, 99987, 186430, 193186, 196081, 234787, 238870, 241138, 265944, 144130, 151757, 153822, 159543, 178077, 227472, 278822, 308932, 176668, 182245, 187100, 218596, 219284, 259707, 271215]
    players_list_eng = [159443, 161715, 236015, 223532, 156365, 155532, 157073, 167127, 157974, 143637, 129358, 241077, 291281, 266696, 127262, 231167, 223453, 238262, 194450, 138924, 250787, 172850, 142200, 230945, 280555, 156366]
    players_list_fra = [148987, 43372, 89018, 196200, 233621, 207015, 251634, 231692, 215378, 277385, 222793, 153053, 285150, 277307, 248676, 176203, 265919, 157675, 46858, 229744, 184012, 88965, 140416, 231388, 222176]
    players_list_ger = [84774, 140740, 122280, 286128, 170209, 174618, 214401, 201803, 249548, 169438, 286828, 186263, 197628, 174550, 131424, 143020, 174617, 190161, 303821, 305554, 274913, 170257, 178980, 231182, 123465, 202641]
    players_list_ira = [252262, 214798, 185648, 320377, 253376, 203453, 194861, 317091, 211717, 180674, 226302, 194870, 211720, 218086, 214800, 194863, 235519, 194865, 188055, 172263, 219610, 226301, 205522, 185827, 219611]
    players_list_jap = [97110, 143697, 253604, 119082, 105803, 157692, 238004, 238050, 202728, 238033, 97111, 157844, 152479, 159348, 219350, 219627, 219362, 256587, 270752, 253173, 274278, 277360, 201469, 274277, 286347, 271352]
    players_list_mor = [175149, 206232, 195240, 240233, 239350, 167686, 245243, 283557, 232461, 292736, 266798, 195226, 223075, 252293, 291552, 336595, 269564, 176733, 242736, 178056, 277865, 300912, 238917, 261089, 185520, 292241]
    players_list_ned = [83802, 190983, 205653, 157892, 159248, 281119, 141443, 126489, 239349, 259863, 282716, 213248, 219022, 168993, 332962, 149577, 146335, 282228, 258968, 159255, 207542, 249524, 177042, 188402, 127420, 255344]
    players_list_pol = [131634, 220853, 179358, 221788, 144288, 234698, 304965, 235180, 176726, 212258, 288488, 165315, 288481, 101958, 177782, 212257, 116632, 190806, 243844, 258067, 268032, 304933, 237666, 220851, 179359, 125824]
    players_list_por = [86758, 181278, 238903, 52767, 176228, 238902, 346588, 234878, 290591, 76717, 176399, 196881, 224144, 124091, 199833, 303785, 157390, 288897, 169402, 208128, 22774, 184423, 258917, 276350, 288896, 109998]
    players_list_qat = [97307, 270844, 219253, 236585, 253337, 219718, 219511, 205377, 156757, 236582, 272874, 310373, 236584, 219254, 270409, 219247, 300011, 172245, 143613, 313131, 263311, 236586, 219258, 219252, 185984, 267954]
    players_list_sau = [247018, 302332, 256611, 268744, 253195, 256667, 236088, 256666, 269485, 251569, 286011, 147037, 253196, 309320, 262468, 291380, 256668, 253408, 270417, 334705, 163850, 271331, 243933, 306690, 177897, 283331]
    players_list_sen = [238362, 154564, 205253, 150312, 224066, 125188, 248668, 137397, 268796, 187608, 144517, 154027, 148172, 255889, 297337, 124228, 301031, 294228, 169797, 241012, 282381, 313889, 268641, 181574, 253992, 308524]
    players_list_ser = [179211, 219531, 192126, 187841, 290375, 197342, 166257, 277119, 219535, 238990, 122575, 174496, 219538, 137076, 222300, 193282, 126752, 211141, 136673, 219536, 240111, 260004, 183209, 221332, 235677, 214433]
    players_list_kor = [175921, 256724, 230244, 185616, 280060, 157688, 158433, 175844, 156769, 228532, 341776, 145673, 185612, 283374, 256598, 270289, 149945, 316511, 274197, 134103, 176322, 276323, 280061, 237224, 303464, 236628]
    players_list_esp = [196176, 108662, 222375, 121021, 265985, 97770, 168531, 128714, 178758, 159317, 251100, 121893, 323702, 140791, 206474, 250465, 231828, 235072, 227765, 195821, 292957, 154446, 297370, 265869, 312146, 154514]
    players_list_swz = [93197, 238544, 258875, 238418, 179233, 214562, 136865, 212237, 175905, 231697, 149981, 152600, 105140, 222628, 222446, 193462, 245623, 303973, 308908, 136775, 259513, 226970, 270641, 238502, 134503, 202099]
    players_list_tun = [215337, 265272, 308627, 174624, 263199, 265099, 230338, 240371, 215336, 195261, 265105, 265234, 191104, 300007, 187249, 231984, 283953, 209595, 254444, 158439, 302944, 148013, 240079, 132241, 169265, 232612]
    players_list_uru = [108622, 184206, 113213, 270821, 103029, 145450, 188398, 104564, 234881, 43711, 158500, 254032, 215772, 251889, 290538, 212973, 241468, 235818, 145600, 241466, 95469, 179767, 67183, 271788, 125088, 67518]
    players_list_usa = [192027, 141316, 303794, 146290, 219273, 266291, 201103, 219275, 222396, 272135, 183778, 183764, 159478, 222776, 256715, 307527, 216617, 259653, 225609, 290230, 251571, 210252, 220474, 225607, 256613, 266027]
    players_list_wal = [83526, 17861, 45548, 241317, 251509, 6327, 85401, 177110, 232325, 291638, 275596, 168695, 93736, 98681, 194801, 24675, 194608, 103469, 288838, 313225, 250478, 77653, 203072, 189605, 291307, 68601]
    players_list_gha = [219562, 266590, 260303, 219309, 186047, 174508, 180573, 276039, 254484, 138171, 277718, 305669, 104030, 266599, 277859, 266057, 189972, 292769, 319775, 123518, 276407, 319767, 273292, 272358, 303115, 214412]
    players_list_mex = [137038, 36363, 103729, 195312, 164331, 245848, 132098, 125300, 224323, 178746, 259975, 241627, 194308, 242715, 104497, 76932, 194311, 146866, 207011, 239990, 242614, 143362, 167060, 200161, 93184, 229487]
    players_list_ecu = [269881, 95614, 207921, 292062, 201531, 214689, 256560, 286665, 204067, 251963, 276615, 287005, 199963, 241245, 262111, 289877, 199038, 328013, 167048, 208046, 277352, 182021, 252702, 281316, 249848, 171771]

    team_name = 'Brazil'
    players_list = players_list_brz
    cursor = connection.cursor()
    team_score = 0
    dim_team_score = 0
    
    print(team_name)

    # G = nx.Graph(team_name=team_name)
    # for player_a, player_b in tqdm(list(combinations(players_list, 2))):
    #     if player_a != player_b:
    #         results = cursor.execute("""SELECT DISTINCT a.player_id AS 'player1',
    #                                                     a.player_type AS 'playerType1',
    #                                                     a.sub_time AS 'subTime1',
    #                                                     b.player_id AS 'player2',
    #                                                     b.player_type AS 'playerType2',
    #                                                     b.sub_time AS 'subTime2',
    #                                                     c.date AS 'date',
    #                                                     d.player_name AS 'playerName1'
    #                                     FROM lineups a 
    #                                     INNER JOIN lineups b ON a.match_id = b.match_id AND a.team_id = b.team_id 
    #                                     INNER JOIN matches c ON c.match_id = a.match_id AND c.match_id = b.match_id
    #                                     INNER JOIN players d ON d.player_id = a.player_id
    #                                     WHERE a.player_id = ? AND b.player_id = ? AND a.player_type != 'Bench' AND b.player_type != 'Bench';""", 
    #                                     (player_a, player_b))
    #         for result in results:
    #             w = get_minutes_played(result)

    #             if G.has_edge(result[0], result[3]):
    #                 G.edges[result[0], result[3]]["weight"] += w
    #             else:
    #                 G.add_edge(result[0], result[3], weight=w)
    #             G.nodes[result[0]]["name"] = result[7]

                # team_score += w

                # original_date = datetime.datetime(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2])) 
                # current_date = datetime.datetime(int(result[6].split('-')[0]), int(result[6].split('-')[1]), int(result[6].split('-')[2])) 
                # date_diff = original_date - current_date
                # years = date_diff.days / 365.25
                # time_weight = math.exp(-0.5 * years)
                # w *= time_weight
                # dim_team_score += w

    # with open('{}.pkl'.format(team_name), 'wb') as f:
    #     pickle.dump(G, f)

    with open('{}.pkl'.format(team_name), 'rb') as f:
        G = pickle.load(f)

        with open('{}.pkl'.format("Argentina"), 'rb') as f:
            G2 = pickle.load(f)

            weights1 = list(zip(*list(G.edges.data("weight"))))[2]
            weights2 = list(zip(*list(G2.edges.data("weight"))))[2]
            weights = weights1 + weights2
            print(len(weights1))
            print(len(weights2))
            print(len(weights))

            G.nodes[258307]["name"] = "Bremer"
            G.nodes[217289]["name"] = "Gabriel Jesus"
            G2.nodes[45843]["name"] = "Lionel Messi"
            print(G.nodes.data("name"))
            pos1 = nx.circular_layout(G)
            pos2 = nx.circular_layout(G2)
            for p in pos2:
                pos2[p][1] -= 2.5

            nx.draw(G, pos=pos1, with_labels=True, labels=dict(G.nodes.data("name")), node_size=1000, width=[w * 10 / max(weights) for w in weights1], node_color="skyblue", node_shape="o", edge_color="grey")
            nx.draw(G2, pos=pos2, with_labels=True, labels=dict(G2.nodes.data("name")), node_size=1000, width=[w * 10 / max(weights) for w in weights2], node_color="skyblue", node_shape="o", edge_color="grey")
            
            # for node in G.edges.data("weight"):
            #     print(node)
            
            # rows = []
            # for node in G.nodes.data("name"):
            #     rows.append([node[0], node[1]])
            # for node in G2.nodes.data("name"):
            #     rows.append([node[0], node[1]])

            # fields = ['id', 'name']
            # with open('nodes_brz_arg.csv', 'w') as f:
            #     write = csv.writer(f)
            #     write.writerow(fields)
            #     write.writerows(rows)

            rows = []
            for edge in G.edges.data("weight"):
                rows.append([edge[0], edge[1], edge[2]])
            for node in G2.edges.data("weight"):
                rows.append([edge[0], edge[1], edge[2]])

            fields = ['id1', 'id2', 'weight']
            with open('edges_brz_arg.csv', 'w') as f:
                write = csv.writer(f)
                write.writerow(fields)
                write.writerows(rows)



            # plt.show()

    print('total minutes: ' + str(team_score))
    print('dim total minutes: ' + str(dim_team_score))

    connection.commit()

    connection.close()

if __name__ == "__main__":
    main()