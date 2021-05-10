import pandas as pd
from helper import sigmoid

data = pd.read_excel('this.xlsx')
headers = ["结果认同-29", "结果认同-30", "结果认同-32"]

all_content = {}

for header in headers:
    all_content[header] = list(data[header])
for i in range(len(all_content["结果认同-29"])):
    try:
        all_content["结果认同-29"][i] = round(sigmoid(all_content["结果认同-29"][i]) * 10, 4)

    except:
        if all_content["结果认同-29"][i] == "比较认同":
            all_content["结果认同-29"][i] = 2
        elif all_content["结果认同-29"][i] == "非常认同":
            all_content["结果认同-29"][i] = 8
for i in range(len(all_content["结果认同-30"])):
    try:
         all_content["结果认同-30"][i] = round(sigmoid(all_content["结果认同-30"][i]) * 10, 4)
    except:
        if all_content["结果认同-30"][i] == "比较认同":
            all_content["结果认同-30"][i] = 2
        elif all_content["结果认同-30"][i] == "非常认同":
            all_content["结果认同-30"][i] = 8
for i in range(len(all_content["结果认同-32"])):
    try:
        all_content["结果认同-32"][i] = round(sigmoid(all_content["结果认同-32"][i]) * 10, 4)
    except:
        if all_content["结果认同-32"][i] == "影响较大":
            all_content["结果认同-32"][i] = 2
        elif all_content["结果认同-32"][i] == "影响非常大":
            all_content["结果认同-32"][i] = 8

all_content['scores'] = []
for i in range(len(all_content["结果认同-32"])):
    all_content['scores'].append(round(
        (all_content["结果认同-29"][i] + all_content["结果认同-30"][i] + all_content["结果认同-32"][i]) / 30, 4))

df = pd.DataFrame(all_content)
df.to_excel("that.xlsx")
