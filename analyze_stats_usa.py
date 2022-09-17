import pickle
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

# everything is home minus away
total_minutes = []
avg_minutes = []
scores = []

# key = match_id
# value = [(home_id, [list of home weights], home_score), (away_id, [list of away weights], away_score), date]

with open('WC_2006.pkl', 'rb') as f:
    stats = pickle.load(f)
    with open('WC_2010.pkl', 'rb') as f:
        stats.update(pickle.load(f))
        with open('WC_2014.pkl', 'rb') as f:
            stats.update(pickle.load(f))
            with open('WC_2018.pkl', 'rb') as f:
                stats.update(pickle.load(f))
                # stats = pickle.load(f)
                for index, match_id in enumerate(stats):
                    # if match_id in upsets:
                    if stats[match_id][0][0] == 660 or stats[match_id][1][0] == 660:
                        # if stats[match_id][0][0] == 660:
                        #     total_minutes.append(sum(stats[match_id][0][1]) - sum(stats[match_id][1][1]))
                        #     avg_minutes.append((sum(stats[match_id][0][1])/len(stats[match_id][0][1])) - (sum(stats[match_id][1][1])/len(stats[match_id][1][1])))
                        #     scores.append(stats[match_id][0][2] - stats[match_id][1][2])
                        # elif stats[match_id][1][0] == 660:
                        #     total_minutes.append(sum(stats[match_id][1][1]) - sum(stats[match_id][0][1]))
                        #     avg_minutes.append((sum(stats[match_id][1][1])/len(stats[match_id][1][1])) - (sum(stats[match_id][0][1])/len(stats[match_id][0][1])))
                        #     scores.append(stats[match_id][1][2] - stats[match_id][0][2])
                        print(match_id)
                        if stats[match_id][0][0] == 660:
                            total_minutes.append((sum(stats[match_id][0][1]) - sum(stats[match_id][1][1])) / (sum(stats[match_id][0][1]) + sum(stats[match_id][1][1])))
                            avg_minutes.append((sum(stats[match_id][0][1])/len(stats[match_id][0][1])) - (sum(stats[match_id][1][1])/len(stats[match_id][1][1])))
                            scores.append(stats[match_id][0][2] - stats[match_id][1][2])
                        elif stats[match_id][1][0] == 660:
                            total_minutes.append((sum(stats[match_id][1][1]) - sum(stats[match_id][0][1])) / (sum(stats[match_id][1][1]) + sum(stats[match_id][0][1])))
                            avg_minutes.append((sum(stats[match_id][1][1])/len(stats[match_id][1][1])) - (sum(stats[match_id][0][1])/len(stats[match_id][0][1])))
                            scores.append(stats[match_id][1][2] - stats[match_id][0][2])

# start = min(scores)
# end = max(scores)
# width = end - start
# res = (arr - arr.min())/(arr.max() - arr.min()) * width + start

# total_minutes = [((x - min(total_minutes))/(max(total_minutes) - min(total_minutes))) * width + start for x in total_minutes]

# scores = [(x - min(scores))/(max(scores) - min(scores)) for x in scores]

scores, total_minutes = (list(t) for t in zip(*sorted(zip(scores, total_minutes))))
scores = np.array(scores)
total_minutes = np.array(total_minutes)
idx   = np.argsort(scores)
scores = np.array(scores)[idx]
total_minutes = np.array(total_minutes)[idx]

r, p = scipy.stats.pearsonr(scores, total_minutes)
print(r, p)
# r, p = scipy.stats.pearsonr(scores, avg_minutes)
# print(r, p)

# x = range(len(scores))
# m, b = np.polyfit(x, scores, 1)
# m2, b2 = np.polyfit(x, total_minutes, 1)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
# ax1.plot(scores, color='black')
# ax1.plot(total_minutes, color='blue')
# ax1.plot(x, m*x+b, color='black')
# ax1.plot(x, m2*x+b2, color='blue')

m, b = np.polyfit(total_minutes, scores, 1)

ax1.plot(total_minutes, m*total_minutes+b, color='black')
ax1.scatter(total_minutes, scores, color='blue', s=20)
ax1.set_xlabel('Chemistry difference')
ax1.set_ylabel('Goal difference')

print(m, b)

plt.show()
