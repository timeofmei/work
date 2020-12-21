import pandas as pd
import ujson
data = pd.read_excel('result/all_content.xlsx')
headers = ['id', 'keyword', 'river', 'district',
           'time', 'source', 'content', 'name', '行政管制工具（如处罚）', '信息沟通工具', '政府与私人合作（ppp）', '法制工具（修订法规）']
fazhi_keywords = '法规，条例，颁布，制定，执法，监督，举报，违法，投诉'.split('，')
all_content = {}
for header in headers:
    all_content[header] = list(data[header])
for i in range(len(all_content['id'])):
    k = 0
    for word in fazhi_keywords:
        if word in all_content['content'][i]:
            k += 1
    if k > 0:
        all_content['法制工具（修订法规）'][i] = 'Y'
    else:
        all_content['法制工具（修订法规）'][i] = 'N'

with open('data/content_all_2.json', 'w') as file:
    json_data = ujson.dumps(all_content, indent=4, ensure_ascii=False)
    file.write(json_data)
