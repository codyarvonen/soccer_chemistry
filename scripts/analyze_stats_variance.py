import pickle
import scipy
import math
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import variance
from sklearn.linear_model import LinearRegression

total_minutes = []
avg_minutes = []
variances = []
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
                    if index % 2 == 0:
                        total_minutes.append((sum(stats[match_id][0][1]) - sum(stats[match_id][1][1])) / (sum(stats[match_id][0][1]) + sum(stats[match_id][1][1])))
                        avg_minutes.append((sum(stats[match_id][0][1])/len(stats[match_id][0][1])) - (sum(stats[match_id][1][1])/len(stats[match_id][1][1])))
                        scores.append(stats[match_id][0][2] - stats[match_id][1][2])
                        dates.append(stats[match_id][2])
                        teams.append((stats[match_id][0][0], stats[match_id][1][0]))

                        variances.append(math.log10(variance(stats[match_id][0][1]) / variance(stats[match_id][1][1])))
                        # variances.append((variance(stats[match_id][0][1]) - variance(stats[match_id][1][1])) / (variance(stats[match_id][0][1]) + variance(stats[match_id][1][1])))
                    else:
                        total_minutes.append((sum(stats[match_id][1][1]) - sum(stats[match_id][0][1])) / (sum(stats[match_id][1][1]) + sum(stats[match_id][0][1])))
                        avg_minutes.append((sum(stats[match_id][1][1])/len(stats[match_id][1][1])) - (sum(stats[match_id][0][1])/len(stats[match_id][0][1])))
                        scores.append(stats[match_id][1][2] - stats[match_id][0][2])
                        dates.append(stats[match_id][2])
                        teams.append((stats[match_id][1][0], stats[match_id][0][0]))
                        
                        variances.append(math.log10(variance(stats[match_id][1][1]) / variance(stats[match_id][0][1])))
                        # variances.append((variance(stats[match_id][1][1]) - variance(stats[match_id][0][1])) / (variance(stats[match_id][1][1]) + variance(stats[match_id][0][1])))

# Reorder the data
scores, total_minutes, dates, teams, variances = (list(t) for t in zip(*sorted(zip(scores, total_minutes, dates, teams, variances))))
scores = np.array(scores)
total_minutes = np.array(total_minutes)
dates = np.array(dates)
teams = np.array(teams)
variances = np.array(variances)
idx   = np.argsort(scores)
scores = np.array(scores)[idx]
total_minutes = np.array(total_minutes)[idx]
dates = np.array(dates)[idx]
teams = np.array(teams)[idx]
variances = np.array(variances)[idx]

# inputs = np.concatenate((total_minutes, variances), axis=0)
inputs = np.column_stack((total_minutes, variances))
# print(inputs)
model = LinearRegression().fit(inputs, scores)
r_sq = model.score(inputs, scores)

print(r_sq)
print(model.intercept_)
print(model.coef_)

# Determine the correlation coefficient
r, p = scipy.stats.pearsonr(scores, variances)
print("Correlation Coefficient: {}".format(r))
print("P-Value: {}".format(p))

# Determine the correlation coefficient
r, p = scipy.stats.pearsonr(scores, total_minutes)
print("Correlation Coefficient: {}".format(r))
print("P-Value: {}".format(p))


print(max(total_minutes), min(total_minutes))
print(max(variances), min(variances))
print(max(total_minutes) - min(total_minutes))
print(max(variances) - min(variances))


# Run the linear regression 
m, b = np.polyfit(variances, scores, 1)

# Plot the data
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(variances, m*variances+b, color='black')
ax1.scatter(variances, scores, color='blue', s=20)
ax1.set_xlabel('Weighted chemistry difference')
ax1.set_ylabel('Goal difference')


plt.show()
