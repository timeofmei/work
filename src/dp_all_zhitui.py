import pandas as pd
import jieba
jieba.initialize()
data = pd.read_excel('data/诉求数据汇总.xlsx')
headers = ["id", "标题", "回复1"]
all_content = {}
zhutui_tools = ["谅解", "感谢您对我们", "民生工程", "难免", "理解", "支持", "水质标准", "需要时间", "民心工程", "信心", "生活品质", "造福", "生态", "高品质", "日夜兼程", "深表歉意", "尽量", "还路于民", "第一时间"]
for header in headers:
    all_content[header] = list(data[header])
all_content["助推工具词频"] = []
all_content["助推工具比重"] = []
for i in range(len(all_content["id"])):
    all_content["助推工具词频"].append(0)
    all_content["助推工具比重"].append(0)
    reply_str = all_content['回复1'][i]
    reply_word_num = len(jieba.lcut(reply_str))
    for tool in zhutui_tools:
        all_content["助推工具词频"][i] += all_content["回复1"][i].count(tool)
        all_content["助推工具比重"][i] += all_content["回复1"][i].count(tool) / reply_word_num
df = pd.DataFrame(all_content)
df.to_excel("zhutui.xlsx")