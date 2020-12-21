import pandas as pd
import ujson
data = pd.read_csv('data/content_all.csv')
gov_sorts = {
    '政府治理-行政处罚': ['罚款', '处罚', '查处', '违规', '出台', '新条例'],
    '政府治理-信息发布': ['决心', '发布', '宣布', '宣告', '表明', '上诉', '上访', '处理', '回应', '沟通', '反映', '处理'],
    '政府治理-PPP': ['联合', '联动', '协作', '合作', '协同', '多部门'],
}
all_content = {
    '关键词': 'keywords',
    '河流': 'rivers',
    '区域': 'districts',
    '作者': 'names',
    '正文': 'articles',
    '时间': 'times',
    '内容源': 'sources'
}
content = {}
for key, value in all_content.items():
    content[value] = list(data[key])
for i in range(len(content['articles'])):
    try:
        if '河' not in content['articles'][i]:
            print(i)
            for val in all_content.values():
                content[val][i] = ''
            continue
    except IndexError:
        pass
for key, value in gov_sorts.items():
    content[key] = []
    for i in range(len(content['articles'])):
        k = 0
        for keyword in value:
            if keyword in content['articles'][i]:
                k += 1
        if k > 0:
            content[key].append('Y')
        else:
            content[key].append('N')
content['id'] = []
for i in range(len(content['articles'])):
    content['id'].append(i)

with open('data/content_all.json', 'w') as file:
    json_data = ujson.dumps(content, indent=4, ensure_ascii=False)
    file.write(json_data)
