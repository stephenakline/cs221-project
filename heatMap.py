import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# https://web.archive.org/web/20150404034126/http://stanford.edu/~mwaskom/software/seaborn/tutorial/dataset_exploration.html
# http://stackoverflow.com/questions/33805689/converting-dictionary-to-dataframe-with-tuple-as-key

results = {}
f = open('sample-data.txt', 'r')
for line in f:
    t = map(float, line.split())
    rounds, sims, memory, pattern, percent = int(t[0]), int(t[1]), int(t[2]), int(t[3]), t[4:]
    results[(memory, pattern)] = sum(t[4:]) / len(t[4:])

numMemory = list(set([i[0] for i in results.keys()]))
numMemory.sort()
numPattern = list(set([i[1] for i in results.keys()]))
numPattern.sort(reverse=True)

data = {}
for j in numMemory:
    temp = []
    for i in numPattern:
        temp.append(results[(j, i)])
    data[j] = temp

df = pd.DataFrame(data)
df = df.set_index([numPattern])

sns.heatmap(df, center=0.5, annot=True);
plt.show()
