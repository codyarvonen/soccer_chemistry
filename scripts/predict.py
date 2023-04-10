import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

include_rank = True
include_chem = True

file_name = 'rank_dim_weight_chem_diff'

chemistry = []
goal_diffs = []
rankings = []

with open(f'../data/data_paper/chemistry_difference/{file_name}.csv') as data_file:
    csv_reader = csv.reader(data_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            chemistry.append(float(row[0]))
            goal_diffs.append(float(row[1]))
            rankings.append(float(row[5]))
        line_count += 1

goals_win = [1 if w > 0 else 0 for w in goal_diffs]
# goals_tie = [1 if w >= 0 else 0 for w in goal_diffs]
goals_los = [1 if w < 0 else 0 for w in goal_diffs]

y_win = np.array(goals_win)
# y_tie = np.array(goals_tie)
y_los = np.array(goals_los)

x = np.transpose([chemistry, rankings])
if not include_rank and include_chem:
    print('Chemistry')
    chems = np.array(chemistry)
    x = chems.reshape(-1,1)
elif not include_chem and include_rank:
    print('Ranking')
    ranks = np.array(rankings)
    x = ranks.reshape(-1,1)
else:
    print('Chem and Rank')

y_win = np.array(goals_win)
# y_tie = np.array(goals_tie)
y_los = np.array(goals_los)

logr = linear_model.LogisticRegression()
logr.fit(x, y_win)

logr2 = linear_model.LogisticRegression()
# logr2.fit(x, y_tie)
logr2.fit(x, y_los)


chems = []
wchem = []
dchem = []
dwchm = []
goals = []
ranks = []

# file_name_2 = '22wc'
file_name_2 = 'WC-2022-team-chemistry'

with open(f'../data/data_paper/chemistry_difference/{file_name_2}.csv') as data_file:
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

goals_win = [1 if w > 0 else 0 for w in goals]
goals_tie = [1 if w >= 0 else 0 for w in goals]
# goals_los = [1 if w < 0 else 0 for w in goals]

# def predict(coefs, inter, x):
#     x2 = coefs * x
#     print(x2.shape)
#     if x2.shape[0] > 1:
#         print('Reshaping')
#         x2 = np.sum(x2, axis=1)
#         x2 = x2.reshape(1, 64)
#     print(x2.shape)
#     log_odds = x2 + inter
#     odds = np.exp(log_odds)
#     probability = odds / (1 + odds)
#     return probability

# Chem
# coef_win = np.array([[1.75893612]])
# coef_tie = np.array([[1.6593807]])
# inter_win = np.array([-0.48765345])
# inter_tie = np.array([0.44226615])
# x = dwchm

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

x = np.transpose([dwchm, ranks])
if not include_rank and include_chem:
    x = np.transpose([dwchm])
elif not include_chem and include_rank:
    x = np.transpose([ranks])
else:
    print('Chem and Rank')


# probs_win = predict(coef_win, inter_win, x)
# probs_noL = predict(coef_tie, inter_tie, x)

# print(x)

probs_win = logr.predict_proba(x)
# probs_noL = logr2.predict_proba(x)
probs_los = logr2.predict_proba(x)

probs_tie = 1 - (probs_win + probs_los)
# probs_los = 1 - (probs_win + probs_tie)


# print(probs_win[:, 1])
print(probs_tie[:, 1])
# print(probs_los[:, 1])

probs_win = probs_win[:, 1]
probs_tie = probs_tie[:, 1]
probs_los = probs_los[:, 1]

# print(probs_win + probs_tie + probs_los)

score = 0

i = 0

for goal_diff in goals:
    print(goal_diff)
    print(probs_win[i])
    print(probs_tie[i])
    print(probs_los[i])
    print()
    if goal_diff > 0:
        # score += probs_win[i]
        if probs_win[i] > probs_los[i] and probs_win[i] > probs_tie[i]:
            score += 1
    if goal_diff < 0:
        # score += probs_los[i]
        if probs_los[i] > probs_win[i] and probs_los[i] > probs_tie[i]:
            score += 1
    if goal_diff == 0:
        # score += probs_tie[i]
        if probs_tie[i] > probs_los[i] and probs_tie[i] > probs_win[i]:
            score += 1
    i += 1

print(score/64)