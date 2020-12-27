import ujson
import pandas as pd
data = pd.read_excel('data/诉求数据汇总.xlsx')
headers = ['id', '标题', '投诉件内容', '回复1']
keywords = {
    'litas': ['公交',  '监督',  '审批',   '小区',  '环境', '儿童',  '紧张',  '安全',
             '隐患',  '护栏',  '散步', '乘凉', '规划', '报警',  '公园',  '违章搭盖', '身体健康'],
    'lijis': ['噪音', '堵', '异味', '污水', '臭水', '气味', '扰民', '损害', '通宵', '居民', '休息'],
    'shengtais': ['生态', '走廊', '景观', '百姓', '群众', '社会', '公众利益',
                 '执行力', '公信力', '监督', '旅游', '形象', '景点', '鸭鹅', '树木']
}

all_content = {}
for header in headers:
    all_content[header] = list(data[header])
all_content['guifan'] = []
for i in range(len(all_content['id'])):
    ks = {
        'litas': 0,
        'lijis': 0,
        'shengtais': 0,
    }
    all = 0
    for key, value in keywords.items():
        for keyword in value:
            if keyword in all_content['投诉件内容'][i]:
                ks[key] += 1
                all += 1
    if all == 0:
        all_content['guifan'].append('无')
    else:
        kmax = max(ks.values())
        for k, v in ks.items():
            if v == kmax:
                all_content['guifan'].append(k)
                break
with open('data/content_suqiu_2.json', 'w') as file:
    json_data = ujson.dumps(all_content, indent=4, ensure_ascii=False)
    file.write(json_data)
