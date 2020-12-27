import pandas as pd
import jieba
positive_words = ['请', '望', '此', '恳', '谢谢']
negative_words = ['！', '!', '？', '?', '难道', '非', '怎么', '到底']
df = pd.read_excel('诉求数据汇总.xlsx')
timecha = df['最终回复-投诉事件'].tolist()
pls = df['投诉件内容'].tolist()
score_mood = []
score_time = []
scorels = []
print("start")

for i in range(len(timecha)):
    score_negative_mood = 1
    score_positive_mood = 1
    score_mood.append(1)
    score_time.append(1 - (pow(timecha[i], 0.5) / 7))
    for letter in jieba.cut(pls[i]):
        if letter in positive_words:
            score_positive_mood *= 1.1
        elif letter in negative_words:
            score_negative_mood *= 1.1
    score_mood[i] = (score_mood[i] * score_positive_mood /
                     score_negative_mood) * 0.75
    score = score_mood[i] * 0.6 + score_time[i] * 0.4
    scorels.append(score)
df['情感倾向'] = scorels
df['内容分数_权值0.6'] = score_mood
df['时间分数_权值0.4'] = score_time
df.to_excel('情感结果.xlsx')
print("done")
