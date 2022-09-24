import pickle
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

total_minutes = []
avg_minutes = []
scores = []

# Team IDs
usa = 660
arg = 202
brz = 205
ger = 481
fra = 478
bel = 459
cro = 477
por = 482
mex = 203
ned = 449

team = ned

weighted = True

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
                    if stats[match_id][0][0] == team or stats[match_id][1][0] == team:
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
idx   = np.argsort(scores)
scores = np.array(scores)[idx]
total_minutes = np.array(total_minutes)[idx]

# Determine the correlation coefficient
r, p = scipy.stats.pearsonr(scores, total_minutes)
print("Correlation Coefficient: {}".format(r))
print("P-Value: {}".format(p))

# Run the linear regression 
m, b = np.polyfit(total_minutes, scores, 1)

# Plot the data
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(total_minutes, m*total_minutes+b, color='black')
ax1.scatter(total_minutes, scores, color='blue', s=20)
ax1.set_xlabel('Chemistry difference')
ax1.set_ylabel('Goal difference')
ax1.set_title('Netherlands')

plt.show()
