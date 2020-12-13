import json
import pandas as pd
river_list = ['洪阵河', '龙津河', '陈厝河', '白湖亭河', '洋里溪', '竹屿河', '瀛洲河', '竹榄河', '大庆河', '台屿河', '淌洋河', '马洲支河', '君竹河', '飞凤河', '泮洋河', '文藻河', '打铁港', '东郊河','安泰河',
              '新透河', '济南河', '磨洋河', '红星河', '茶园河', '琴亭河', '三捷河', '跃进河', '半洋亭河', '洋下河', '牛浦河', '浦东河', '浦上河', '阳岐河', '光明港二支河', '潘墩河', '金港河', '达道河', '梅峰河', '吴山河']
fuzhou_districts = ['鼓楼', '台江', '仓山', '晋安', '马尾', '长乐']
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
rivers = []
districts = []
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
for i in range(len(keywords)):
    k = 0
    for river in river_list:
        if river in articles[i] or river in names[i]:
            k += 1
            try:
                temp = rivers[i]
                temp += f',{river}'
                rivers[i] = temp
            except IndexError:
                rivers.append(river)
    if k == 0:
        rivers.append('未分类')
assert len(keywords) == len(names) == len(
    articles) == len(times) == len(sources)
for i in range(len(keywords)):
    k = 0
    for district in fuzhou_districts:
        if district in articles[i]:
            k += 1
            try:
                temp = districts[i]
                temp += f',{district}'
                districts[i] = temp
            except IndexError:
                districts.append(district)
    if k == 0:
        districts.append('未分类')
assert len(keywords) == len(names) == len(
    articles) == len(times) == len(sources)
all_content = {
    '关键词': keywords,
    '河流': rivers,
    '区域': districts,
    '作者': names,
    '正文': articles,
    '时间': times,
    '内容源': sources
}
frame = pd.DataFrame(all_content)
frame.to_csv('data/content_all.csv', encoding="utf_8_sig")
