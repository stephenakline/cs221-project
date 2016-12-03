import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# https://web.archive.org/web/20150404034126/http://stanford.edu/~mwaskom/software/seaborn/tutorial/dataset_exploration.html
# http://stackoverflow.com/questions/33805689/converting-dictionary-to-dataframe-with-tuple-as-key

results = {}
timesWon = {}
f = open('simResults.txt', 'r')
for line in f:
    t = map(float, line.split())
    if len(t) == 0: continue
    rounds, sims, memory, pattern, percent = int(t[0]), int(t[1]), int(t[2]), int(t[3]), t[4:]
    results[(memory, pattern)] = sum(t[4:]) / len(t[4:])
    timesWon[(memory, pattern)] = len([x for x in t[4:] if x > .5]) / float(sims)

numMemory = list(set([i[0] for i in results.keys()]))
numMemory.sort()
numPattern = list(set([i[1] for i in results.keys()]))
numPattern.sort(reverse=True)

percentData = {}
winData = {}
for j in numMemory:
    temp1 = []
    temp2 = []
    for i in numPattern:
        temp1.append(results[(j, i)])
        temp2.append(timesWon[(j, i)])
    percentData[j] = temp1
    winData[j] = temp2

df = pd.DataFrame(percentData)
df = df.set_index([numPattern])

figure = plt.gcf() # get current figure
figure.set_size_inches(11, 8.5)

# sns.heatmap(df, center=0.5, annot=True, vmin=0, vmax=1.0, \
sns.heatmap(df, center=0.5, annot=True, \
    linecolor="grey", linewidths=1);
plt.title('Percentage of %s Rounds Won Across %s Games' % (rounds, sims), fontsize=18)
plt.xlabel('Length of Short Term Memory (n)', fontsize=14)
plt.ylabel('Length of Max Pattern (p_init)', fontsize=14)
plt.savefig('percent-rounds-won.png')

plt.clf()

df = pd.DataFrame(winData)
df = df.set_index([numPattern])

figure = plt.gcf() # get current figure
figure.set_size_inches(11, 8.5)
sns.heatmap(df, center=0.5, annot=True, vmin=0, vmax=1.0, \
# sns.heatmap(df, center=0.5, annot=True, \
    cmap="Greys", linecolor="grey", linewidths=1);
plt.title('Percentage of %s Games Won' % sims, fontsize=18)
plt.xlabel('Length of Short Term Memory (n)', fontsize=14)
plt.ylabel('Length of Max Pattern (p_init)', fontsize=14)
plt.savefig('percent-games-won.png')
