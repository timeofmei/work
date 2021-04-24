import jieba
import math
import pandas as pd
positive_words = ['请', '望', '此', '恳', '谢谢']
negative_words = ['！', '!', '？', '?', '难道', '非', '怎么', '到底']
df = pd.read_excel('data/新诉求数据.xlsx')
timecha = df['最终回复-投诉事件'].tolist()
pls = df['诉求件内容'].tolist()
score_mood = []
score_time = []
scorels = []
print("start")

for i in range(len(timecha)):
    score_negative_mood = 1
    score_positive_mood = 1
    v1 = 0
    score_mood.append(1)
    score_time.append(1 - (pow(timecha[i], 0.5) / 7))
    for letter in jieba.cut(pls[i]):
        if letter in positive_words:
            v1 += 1
        elif letter in negative_words:
            v1 -= 1
    score_mood[i] = 0.1 * math.exp(v1)
    if score_mood[i] > 1:
        score_mood[i] = 1
    score = score_mood[i] * 0.6 + score_time[i] * 0.4
    if score > 1:
        score = 1
    scorels.append(score)
df['情感倾向'] = scorels
df['内容分数_权值0.6'] = score_mood
df['时间分数_权值0.4'] = score_time
df.to_excel('新情感结果.xlsx')
print("done")
