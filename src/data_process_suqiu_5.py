import pandas as pd
import ujson

data = pd.read_excel("data/诉求数据汇总.xlsx")
headers = ["结果认同-29", "结果认同-30", "结果认同-32"]

all_content = {}

for header in headers:
    all_content[header] = list(data[header])
for i in range(len(all_content["结果认同-29"])):
    try:
        all_content["结果认同-29"][i] += 5
        if all_content["结果认同-29"][i] > 10:
            all_content["结果认同-29"][i] = 10
    except:
        if all_content["结果认同-29"][i] == "比较认同":
            all_content["结果认同-29"][i] = 3
        elif all_content["结果认同-29"][i] == "非常认同":
            all_content["结果认同-29"][i] = 7
for i in range(len(all_content["结果认同-30"])):
    try:
        all_content["结果认同-30"][i] += 5
        if all_content["结果认同-30"][i] > 10:
            all_content["结果认同-30"][i] = 10
    except:
        if all_content["结果认同-30"][i] == "比较认同":
            all_content["结果认同-30"][i] = 4
        elif all_content["结果认同-30"][i] == "非常认同":
            all_content["结果认同-30"][i] = 6
for i in range(len(all_content["结果认同-32"])):
    try:
        all_content["结果认同-32"][i] += 2
        if all_content["结果认同-32"][i] > 10:
            all_content["结果认同-32"][i] = 10
    except:
        if all_content["结果认同-32"][i] == "影响较大":
            all_content["结果认同-32"][i] = 4
        elif all_content["结果认同-32"][i] == "影响非常大":
            all_content["结果认同-32"][i] = 7

all_content['scores'] = []
for i in range(len(all_content["结果认同-32"])):
    all_content['scores'].append(
        (all_content["结果认同-29"][i] + all_content["结果认同-30"][i] + all_content["结果认同-32"][i]) / 30)
with open('data/content_suqiu_5.json', 'w') as file:
    json_data = ujson.dumps(all_content, indent=4, ensure_ascii=False)
    file.write(json_data)
