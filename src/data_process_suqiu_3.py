import ujson
import pandas as pd
data = pd.read_excel('data/诉求数据汇总.xlsx')
headers = ['id', '标题', '投诉件内容', '回复1']
kongzhis = ['匿名', '实名']
all_content = {}
for header in headers:
    all_content[header] = list(data[header])
all_content['kongzhi'] = []
for i in range(len(all_content['id'])):
    all_content['kongzhi'].append('')
    content_str = all_content['投诉件内容'][i]
    if '匿名' in content_str:
        all_content['kongzhi'][i] += 'niming '
    if '实名' in content_str:
        all_content['kongzhi'][i] += 'shiming'
    if all_content['kongzhi'][i] == '':
        all_content['kongzhi'][i] += 'wu'
with open('data/content_suqiu_3.json', 'w') as file:
    json_data = ujson.dumps(all_content, indent=4, ensure_ascii=False)
    file.write(json_data)
