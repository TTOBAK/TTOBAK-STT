import os, glob
import json

results = glob.glob('result1/*.json')
results.sort()

phone_score = 0.0
word_score = 0.0
text_score = 0.0

for i in range(0, 247):
    file = open(results[i])
    data = json.load(file)
    score = float(data['score'])
    text = data['transcript']
    file.close()


    if i >= 0 and i < 47: phone_score += score
    elif i >= 47 and i < 147: word_score += score
    else: text_score += score

    print(i, text, score)

phone_score = phone_score / 47.0
word_score = word_score / 100.0
text_score = text_score / 100.0

print('\n----------------------------------')
print('Average Score')
print('----------------------------------\n')
print('Tested Phone-Level Scripts : 47')
print('Tested Word-Level Scripts : 100')
print('Tested Sentence-Level Scripts : 100\n')
print('Phone-Level Script Score: ', phone_score)
print('Word-Level Scripts: ', word_score)
print('Sentence-Level Scripts:', text_score)
