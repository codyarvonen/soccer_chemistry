import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

include_rank = True
include_chem = False

chems = []
goals = []
ranks = []

file_name = 'rank_weight_chem_diff'

print(file_name)

with open(f'../data/data_paper/chemistry_difference/{file_name}.csv') as data_file:
    csv_reader = csv.reader(data_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            chems.append(float(row[0]))
            goals.append(float(row[1]))
            ranks.append(float(row[5]))
        line_count += 1

goals_win = [1 if w > 0 else 0 for w in goals]
goals_tie = [1 if w >= 0 else 0 for w in goals]

x = np.transpose([chems, ranks])
if not include_rank and include_chem:
    print('Chemistry')
    chems = np.array(chems)
    x = chems.reshape(-1,1)
elif not include_chem and include_rank:
    print('Ranking')
    ranks = np.array(ranks)
    x = ranks.reshape(-1,1)
else:
    print('Chem and Rank')

y_win = np.array(goals_win)
y_tie = np.array(goals_tie)

logr = linear_model.LogisticRegression()
logr.fit(x, y_win)

logr2 = linear_model.LogisticRegression()
logr2.fit(x, y_tie)

def logit2prob(logr, x):
  log_odds = logr.coef_ * x + logr.intercept_
  odds = np.exp(log_odds)
  probability = odds / (1 + odds)
  print('Intercept, Coefficients')
  print(logr.intercept_, logr.coef_)
  return probability

print('Winning')
prob = logit2prob(logr, x)
print('Not Loosing')
prob2 = logit2prob(logr2, x)

# prob = list(prob)
# prob2 = list(prob2)
# prob, prob2, ranks = (list(t) for t in zip(*sorted(zip(prob, prob2, ranks))))


# fig = plt.figure()
# ax1 = fig.add_subplot(1, 1, 1)
# ax1.plot(ranks, prob, color='black')
# ax1.plot(ranks, prob2, color='blue')
# ax1.axhline(y=0.5, color='red')

# ax1.set_xlabel('Logistic weighted chemistry difference')
# ax1.set_ylabel('Probability of winning')

# plt.show()
