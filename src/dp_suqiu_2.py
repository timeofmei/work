import pandas as pd
from random import choice
data = pd.read_excel('data/诉求数据汇总.xlsx')
headers = ['id', '标题', '投诉件内容', '回复1']
keywords = {
    '利他': {'大家': 2, '公交': 1,  '监督': 1,  '审批': 1,  '环境': 2, '儿童': 2,  '紧张': 1,  '安全': 1,
              '隐患': 3,  '护栏': 1,  '散步': 1, '乘凉': 2, '规划': 1, '报警': 1,  '公园': 1,  '违章': 1, '健康': 2, '完工': 1, '工期': 1, '您': 3, '请问': 3},
    '利己': {'噪音': 1, '堵': 2, '异味': 2, '污水': 2, '臭水': 2, '气味': 1, '扰民': 1, '损害': 1, '通宵': 2, '居民': 1, '休息': 1, '!!': 3, '！！': 3},
    '生态': {'生态': 3, '走廊': 1, '景观': 2, '百姓': 2, '群众': 2, '社会': 2, '公众': 2,
                  '执行力': 1, '公信力': 1, '监督': 1, '旅游': 2, '形象': 1, '景点': 1, '鸭鹅': 2, '树木': 2,  '环境': 3}
}

all_content = {}
all_content['liji_score'] = []
all_content['lita_score'] = []
all_content['shengtai_score'] = []
for header in headers:
    all_content[header] = list(data[header])
all_content['guifan'] = []
for i in range(len(all_content['id'])):
    ks = {
        '利他': 0,
        '利己': 0,
        '生态': 0,
    }
    all = 0
    num = 0
    if len(all_content['投诉件内容'][i]) <= 30:
        all_content['guifan'].append('利己')
        all_content['liji_score'].append(6)
        all_content['lita_score'].append(0)
        all_content['shengtai_score'].append(0)
        continue
    elif len(all_content['投诉件内容'][i]) >= 200:
        all_content['guifan'].append('利他')
        all_content['liji_score'].append(0)
        all_content['lita_score'].append(6)
        all_content['shengtai_score'].append(0)
        continue
    for key, value in keywords.items():
        for keyword, weight in value.items():
            if keyword in all_content['投诉件内容'][i]:
                ks[key] += weight
                all += 1
    if all == 0:
        all_content['guifan'].append(choice(['利己', '利他', '生态', '利己']))
        all_content['liji_score'].append(0)
        all_content['lita_score'].append(0)
        all_content['shengtai_score'].append(0)
    else:
        all_content['guifan'].append('')
        all_content['liji_score'].append(ks['利己'])
        all_content['lita_score'].append(ks['利他'])
        all_content['shengtai_score'].append(ks['生态'])
        kmax = max(ks.values())
        for k, v in ks.items():
            if v == kmax:
                num += 1
                all_content['guifan'][i] += f'{k} '
        if num > 1:
            all_content['guifan'][i] = choice([all_content['guifan'][i].split(' ')[0], all_content['guifan'][i].split(' ')[1]])
df = pd.DataFrame(all_content)
df.to_excel("hi.xlsx")
