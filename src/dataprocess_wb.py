import pandas as pd
import json

keywords = '黑臭 生活垃圾 内河整治 信访举报 生态环保督察 水资源保护 水域岸线管理 水污染防治 水环境治理 水生态修复 排污口 雨污口 截污管网 抽样监测 清淤 底泥'.split(
    ' ')
official_name = ['福建', '福州', '榕城', '鼓楼', '台江', '仓山', '晋安', '马尾', '长乐']
id = 0
all_content = {}
for keyword in keywords:
    content = {}
    route = f'/Users/timeofmei/Documents/work/weibo-search/结果文件/{keyword} 福州/{keyword} 福州.csv'
    df = pd.read_csv(route)
    nicknames = list(df['用户昵称'])
    tweets = list(df['微博正文'])
    times = list(df['发布时间'])
    try:
        assert len(nicknames) == len(tweets) and len(nicknames) == len(times)
    except:
        print(f"重新处理{keyword}")
        continue
    for i in range(len(nicknames)):
        index = 0
        for name in official_name:
            if name in nicknames[i]:
                index += 1
        if index == 0:
            continue
        id += 1
        content[str(id)] = {}
        content[str(id)]['id'] = id
        content[str(id)]['keyword'] = keyword
        content[str(id)]['用户昵称'] = nicknames[i]
        content[str(id)]['微博正文'] = tweets[i]
        content[str(id)]['发布时间'] = times[i]
    all_content[keyword] = content
    print(f'{keyword} done')

with open('content_wb.json', 'w') as file:
    data = json.dumps(all_content, indent=4, separators=(
        ',', ': '), ensure_ascii=False)
    file.write(data)
print("done")
