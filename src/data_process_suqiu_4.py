import ujson
import pandas as pd
data = pd.read_excel('C:\\Users\\jingjing\\Desktop\\h.xlsx')
headers = ['id', '标题', '投诉件内容', '回复1']
all_words = {
    '29比较认同': ['扰民', '施工单位', '隐患', '规范'],
    '29非常认同': ['偷工减料', '良心', '严查', '无良', '违反', '合同', '极差'],
    '30比较认同': ['望采纳', '建议', '希望', '尽快', '帮助'],
    '30非常认同': ['实事求是', '为民办实事', '推脱', '中央巡视组', '严查', '严肃'],
    '32影响较大': ['建议', '咨询', '请问', '谢谢', '路灯', '何时'],
    '32影响非常大': ['严重', '投诉', '崩溃', '公示', '勘察', '举报', '求助', '良心', '恶臭']
}
all_content = {}
for header in headers:
    all_content[header] = list(data[header])
for k in all_words.keys():
    all_content[k] = []
for i in range(len(all_content['id'])):
    for key, value in all_words.items():
        all_content[key].append(0)
        for word in value:
            if word in all_content['投诉件内容'][i]:
                all_content[key][i] += 1

with open('data/content_suqiu_4_t.json', 'w') as file:
    json_data = ujson.dumps(all_content, indent=4, ensure_ascii=False)
    file.write(json_data)
