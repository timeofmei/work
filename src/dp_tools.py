import pandas as pd
data = pd.read_excel("~/Desktop/诉求数据0528.xlsx")
headers = ["id", "政府工具", "行政工具词频", "信息工具词频", "合作工具词频", "法制工具词频", "助推工具词频"]
all_content = {}
all_content["政府工具_new"] = []
for header in headers:
    all_content[header] = list(data[header])
all_content["政府工具_new"] = ["" for _ in range(len(all_content["id"]))]
for i in range(len(all_content["id"])):
    maxCiPin = max(all_content["行政工具词频"][i], all_content["信息工具词频"][i], all_content["合作工具词频"][i], all_content["法制工具词频"][i], all_content["助推工具词频"][i])
    if maxCiPin == 0:
        all_content["政府工具_new"][i] = all_content["政府工具"][i]
        continue
    for header in headers[2:]:
        if all_content[header][i] == maxCiPin:
            all_content["政府工具_new"][i] += f"{header[:2]} "

df = pd.DataFrame(all_content)
df.to_excel("tools.xlsx")