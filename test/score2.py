import os, glob
import json

results = glob.glob('result2/*.json')
results.sort()

total = 0.0

for i in range(len(results)):
    file = open(results[i])
    data = json.load(file)
    score = float(data['score'])
    text = data['transcript']
    file.close()

    print(i, text, score)
    total += score


print('\n----------------------------------')
print('Average Score')
print(total / len(results))
