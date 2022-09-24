import pickle
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

weighted = True

total_minutes = []
avg_minutes = []
scores = []

# Gather the data from the pickle files
# Here is how the data is formated:
# Dictionary = {key: value} 
#   with
# key = match_id
#   and 
# value = [(home_id, [list of home weights], home_score), (away_id, [list of away weights], away_score), date]

with open('../data/WC_2006.pkl', 'rb') as f:
    stats = pickle.load(f)
    with open('../data/WC_2010.pkl', 'rb') as f:
        stats.update(pickle.load(f))
        with open('../data/WC_2014.pkl', 'rb') as f:
            stats.update(pickle.load(f))
            with open('../data/WC_2018.pkl', 'rb') as f:
                stats.update(pickle.load(f))
                for index, match_id in enumerate(stats):
                    # Calculate the chemistry differences
                    if weighted:
                        if index % 2 == 0:
                            total_minutes.append((sum(stats[match_id][0][1]) - sum(stats[match_id][1][1])) / (sum(stats[match_id][0][1]) + sum(stats[match_id][1][1])))
                            avg_minutes.append((sum(stats[match_id][0][1])/len(stats[match_id][0][1])) - (sum(stats[match_id][1][1])/len(stats[match_id][1][1])))
                            scores.append(stats[match_id][0][2] - stats[match_id][1][2])
                        else:
                            total_minutes.append((sum(stats[match_id][1][1]) - sum(stats[match_id][0][1])) / (sum(stats[match_id][1][1]) + sum(stats[match_id][0][1])))
                            avg_minutes.append((sum(stats[match_id][1][1])/len(stats[match_id][1][1])) - (sum(stats[match_id][0][1])/len(stats[match_id][0][1])))
                            scores.append(stats[match_id][1][2] - stats[match_id][0][2])
                    else:
                        if index % 2 == 0:
                            total_minutes.append(sum(stats[match_id][0][1]) - sum(stats[match_id][1][1]))
                            avg_minutes.append((sum(stats[match_id][0][1])/len(stats[match_id][0][1])) - (sum(stats[match_id][1][1])/len(stats[match_id][1][1])))
                            scores.append(stats[match_id][0][2] - stats[match_id][1][2])
                        else:
                            total_minutes.append(sum(stats[match_id][1][1]) - sum(stats[match_id][0][1]))
                            avg_minutes.append((sum(stats[match_id][1][1])/len(stats[match_id][1][1])) - (sum(stats[match_id][0][1])/len(stats[match_id][0][1])))
                            scores.append(stats[match_id][1][2] - stats[match_id][0][2])

# Reorder the data
scores, total_minutes = (list(t) for t in zip(*sorted(zip(scores, total_minutes))))
scores = np.array(scores)
total_minutes = np.array(total_minutes)
idx = np.argsort(scores)
scores = np.array(scores)[idx]
total_minutes = np.array(total_minutes)[idx]

matches = tuple(zip(total_minutes, scores))

bin_size = 0
if weighted:
    bin_size = 0.33
else:
    bin_size = 25000

# Organize the data into bins
minutes = []
bins = np.arange(min(total_minutes), max(total_minutes), bin_size)
for i in range(1, len(bins)):
    indices = np.digitize(total_minutes, bins) == i
    result = [matches[x] for x, i in enumerate(indices) if i == True]
    minutes.append(result)

# Calculate the probabilities for each bin
probability_of_winning = []
probability_of_not_loosing = []
for games in minutes:
    wins = 0
    losses = 0
    draws = 0
    for game in games:
        if game[1] > 0:
            wins += 1
        elif game[1] < 0:
            losses += 1
        else:
            draws += 1
    if len(games) < 1:
        probability_of_winning.append(0.5)
        probability_of_not_loosing.append(0.5)
    else:
        probability_of_winning.append(wins / (wins + losses + draws))
        probability_of_not_loosing.append((wins + draws) / (wins + losses + draws))

# Determine the correlation coefficient
r, p = scipy.stats.pearsonr(scores, total_minutes)
print("Correlation Coefficient: {}".format(r))
print("P-Value: {}".format(p))

# Plot the data
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(bins[1:], probability_of_winning, color='black', label='Probability of winning')
ax1.plot(bins[1:], probability_of_not_loosing, color='blue', label='Probability of not loosing')
ax1.axhline(y=0.5, color='red')
ax1.set_xlabel('Chemistry difference')
ax1.set_ylabel('Probability')
ax1.legend()

plt.show()

