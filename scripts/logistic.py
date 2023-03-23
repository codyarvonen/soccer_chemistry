import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

include_rank = True
include_chem = True

chem = []
goals = []
ranks = []

with open('../data/data_paper/chemistry_difference/rank_chem_diff.csv') as data_file:
    csv_reader = csv.reader(data_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            chem.append(float(row[0]))
            goals.append(float(row[1]))
            ranks.append(float(row[5]))
        line_count += 1

x = np.array(chem)
x2 = np.array(ranks)
goal = [1 if w > 0 else 0 for w in goals]
goal2 = [1 if w >= 0 else 0 for w in goals]
y = np.array(goal)
y2 = np.array(goal2)

# Reorder the data
chem, goal, goal2, ranks = (list(t) for t in zip(*sorted(zip(chem, goal, goal2, ranks))))
chem = np.array(chem)
goal = np.array(goal)
goal2 = np.array(goal2)
ranks = np.array(ranks)
idx   = np.argsort(chem)
chem = np.array(chem)[idx]
ranks = np.array(ranks)[idx]
goal = np.array(goal)[idx]
goal2 = np.array(goal2)[idx]

# idx_r   = np.argsort(ranks)
# chem_r = np.array(chem)[idx_r]
# ranks_r = np.array(ranks)[idx_r]
# goal_r = np.array(goal)[idx_r]
# goal2_r = np.array(goal2)[idx_r]


x1 = chem.reshape(-1,1)
x2 = ranks.reshape(-1,1)
y = np.array(goal)
y2 = np.array(goal2)

x = x1
if not include_chem and include_rank:
  x = x2
elif include_chem and include_rank:
  x = np.transpose([chem, ranks])

logr = linear_model.LogisticRegression()
logr.fit(x, y)

logr2 = linear_model.LogisticRegression()
logr2.fit(x, y2)

def logit2prob(logr, x):
  log_odds = logr.coef_ * x + logr.intercept_
  odds = np.exp(log_odds)
  probability = odds / (1 + odds)
  print(logr.intercept_, logr.coef_)
  return probability

prob = logit2prob(logr, x)
prob2 = logit2prob(logr2, x)
# print(prob)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(chem, prob, color='black')
ax1.plot(chem, prob2, color='blue')
ax1.axhline(y=0.5, color='red')
# ax1.axvline(x=, color='red')
# ax1.axvline(, color='red')
ax1.set_xlabel('Logistic weighted chemistry difference')
ax1.set_ylabel('Probability of winning')

plt.show()
