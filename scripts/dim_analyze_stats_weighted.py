import pickle
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import csv

total_minutes = []
avg_minutes = []
scores = []
dates = []
teams = []

save_csv = False

# Gather the data from the pickle files
# Here is how the data is formated:
# Dictionary = {key: value} 
#   with
# key = match_id
#   and 
# value = [(home_id, [list of home weights], home_score), (away_id, [list of away weights], away_score), date]

with open('../data/dim_WC_2018.pkl', 'rb') as f:
    stats = pickle.load(f)
    with open('../data/dim_WC_2014.pkl', 'rb') as f:
        stats.update(pickle.load(f))
        with open('../data/dim_WC_2010.pkl', 'rb') as f:
            stats.update(pickle.load(f))
            with open('../data/dim_WC_2006.pkl', 'rb') as f:
                stats.update(pickle.load(f))
                for index, match_id in enumerate(stats):
                    # Calculate the chemistry differences
                    if index % 2 == 0:
                        total_minutes.append((sum(stats[match_id][0][1]) - sum(stats[match_id][1][1])) / (sum(stats[match_id][0][1]) + sum(stats[match_id][1][1])))
                        avg_minutes.append((sum(stats[match_id][0][1])/len(stats[match_id][0][1])) - (sum(stats[match_id][1][1])/len(stats[match_id][1][1])))
                        scores.append(stats[match_id][0][2] - stats[match_id][1][2])
                        dates.append(stats[match_id][2])
                        teams.append((stats[match_id][0][0], stats[match_id][1][0]))
                    else:
                        total_minutes.append((sum(stats[match_id][1][1]) - sum(stats[match_id][0][1])) / (sum(stats[match_id][1][1]) + sum(stats[match_id][0][1])))
                        avg_minutes.append((sum(stats[match_id][1][1])/len(stats[match_id][1][1])) - (sum(stats[match_id][0][1])/len(stats[match_id][0][1])))
                        scores.append(stats[match_id][1][2] - stats[match_id][0][2])
                        dates.append(stats[match_id][2])
                        teams.append((stats[match_id][1][0], stats[match_id][0][0]))

# Reorder the data
scores, total_minutes, dates, teams = (list(t) for t in zip(*sorted(zip(scores, total_minutes, dates, teams))))
scores = np.array(scores)
total_minutes = np.array(total_minutes)
dates = np.array(dates)
teams = np.array(teams)
idx   = np.argsort(scores)
scores = np.array(scores)[idx]
total_minutes = np.array(total_minutes)[idx]
dates = np.array(dates)[idx]
teams = np.array(teams)[idx]

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
ax1.set_xlabel('Weighted relative chemistry difference')
ax1.set_ylabel('Goal difference')

# Save the data
if save_csv:
    rows = []
    for x in range(len(total_minutes)):
        rows.append([total_minutes[x], scores[x], teams[x][0], teams[x][1], dates[x]])

    fields = ['weight_chem_diff', 'goal_diff', 'team_1', 'team_2', 'date']
    with open('../data/dim_weight_chem_diff.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)

plt.show()
