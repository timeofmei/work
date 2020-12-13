import json
import pandas as pd
with open('data/content_wb.json') as file:
    data_wb = json.load(file)
with open('data/content_fzrb.json') as file:
    data_fzrb = json.load(file)
with open('data/content_dnw.json') as file:
    data_dnw = json.load(file)
keywords = []
names = []
articles = []
times = []
sources = []
for keyword, ids in data_wb.items():
    for content in ids.values():
        keywords.append(content['keyword'])
        names.append(content['用户昵称'])
        articles.append(content['微博正文'])
        times.append(content['发布时间'][:10])
        sources.append('微博')
assert len(keywords) == len(names) == len(
    articles) == len(times) == len(sources)
for time_keyword, content in data_fzrb.items():
    time, keyword = time_keyword.split('_')
    time = time[:4] + '-' + time[4:6] + '-' + time[6:]
    keywords.append(keyword)
    times.append(time)
    articles.append(content[2:])
    names.append('福州日报社')
    sources.append('福州日报')
assert len(keywords) == len(names) == len(
    articles) == len(times) == len(sources)
for keyword, biaotis in data_dnw.items():
  for content in biaotis.values():
    keywords.append(keyword)
    names.append('东南网')
    articles.append(content['biaoti'] + content['article'])
    times.append(content['time'])
    sources.append('东南网')
assert len(keywords) == len(names) == len(
    articles) == len(times) == len(sources)
all_content = {
  '关键词': keywords,
  '作者': names,
  '正文': articles,
  '时间': times,
  '内容源': sources
}
frame = pd.DataFrame(all_content)
frame.to_csv('data/content_all.csv', encoding="utf_8_sig")
