import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

include_rank = True
include_chem = False

chems = []
wchem = []
dchem = []
dwchm = []
goals = []
ranks = []

file_name = '22wc'

with open(f'../data/data_paper/chemistry_difference/{file_name}.csv') as data_file:
    csv_reader = csv.reader(data_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            chems.append(float(row[0]))
            wchem.append(float(row[1]))
            dchem.append(float(row[2]))
            dwchm.append(float(row[3]))
            goals.append(float(row[4]))
            ranks.append(float(row[8]))
        line_count += 1

# goals_win = [1 if w > 0 else 0 for w in goals]
# goals_tie = [1 if w >= 0 else 0 for w in goals]

def predict(coefs, inter, x):
    x2 = coefs * x
    print(x2.shape)
    if x2.shape[0] > 1:
        print('Reshaping')
        x2 = np.sum(x2, axis=1)
        x2 = x2.reshape(1, 64)
    print(x2.shape)
    log_odds = x2 + inter
    odds = np.exp(log_odds)
    probability = odds / (1 + odds)
    return probability

# Chem
coef_win = np.array([[1.75893612]])
coef_tie = np.array([[1.6593807]])
inter_win = np.array([-0.48765345])
inter_tie = np.array([0.44226615])
x = dwchm

# Rank
# inter_win = np.array([-0.49932678] )
# coef_win = np.array([[0.00229519]])
# inter_tie = np.array([0.46550979])
# coef_tie = np.array([[0.00239547]])
# x = ranks

# Both
# inter_win = np.array([-0.50131778])
# coef_win = np.array([[1.15122705, 0.00165162]])
# inter_tie = np.array([0.48717084])
# coef_tie = np.array([[0.97430732, 0.0018289 ]])
# x = np.transpose([dwchm, ranks])


probs_win = predict(coef_win, inter_win, x)
probs_noL = predict(coef_tie, inter_tie, x)

probs_tie = probs_noL - probs_win
probs_los = 1 - (probs_win + probs_tie)


# print(probs_win)
# print(probs_tie)
# print(probs_los)

print(probs_win + probs_tie + probs_los)

score = 0

i = 0

for goal_diff in goals:
    if goal_diff > 0:
        score += probs_win[0][i]
    if goal_diff < 0:
        score += probs_los[0][i]
    if goal_diff == 0:
        score += probs_tie[0][i]
    i += 1

print(score/64)