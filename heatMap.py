import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# https://web.archive.org/web/20150404034126/http://stanford.edu/~mwaskom/software/seaborn/tutorial/dataset_exploration.html
# http://stackoverflow.com/questions/33805689/converting-dictionary-to-dataframe-with-tuple-as-key
# http://seaborn.pydata.org/examples/many_pairwise_correlations.html

'''
dont show when p >= n
'''

results = {}
timesWon = {}
f = open('simResults_5.txt', 'r')
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

mask = np.zeros_like(df, dtype=np.bool)
for pattern, row in df.iterrows():
    for memory in row.index:
        if pattern >= memory:
            rowindex = numPattern.index(pattern)
            colindex = numMemory.index(memory)
            mask[rowindex, colindex] = True

figure = plt.gcf() # get current figure
figure.set_size_inches(11, 8.5)

sns.heatmap(df, cmap='RdBu_r', annot=True, mask=mask)
# sns.heatmap(df, center=0.5, mask=mask)
plt.title('Average of %s Rounds Won Across %s Games - Opponent with delta = 5' % (rounds, sims), fontsize=18)
plt.xlabel('Length of Short Term Memory (n)', fontsize=14)
plt.ylabel('Length of Max Pattern (p_init)', fontsize=14)
plt.savefig('percent-rounds-won-5.png')

plt.clf()

df = pd.DataFrame(winData)
df = df.set_index([numPattern])

figure = plt.gcf() # get current figure
figure.set_size_inches(11, 8.5)
sns.heatmap(df, cmap='RdBu_r', annot=True,  mask=mask)
# sns.heatmap(df, center=0.5, vmin=0.2, vmax=0.8, mask=mask)
plt.title('Percentage of %s Games Won - Opponent with delta = 5' % sims, fontsize=18)
plt.xlabel('Length of Short Term Memory (n)', fontsize=14)
plt.ylabel('Length of Max Pattern (p_init)', fontsize=14)
plt.savefig('percent-games-won-5.png')
