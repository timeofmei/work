import httpx
from fake_useragent import UserAgent
from lxml import etree
import json
base_url = "https://mag.fznews.com.cn/fzrb/2020"
keywords = '黑臭 生活垃圾 内河整治 信访举报 生态环保督察 水资源保护 水域岸线管理 水污染防治 水环境治理 水生态修复 排污口 雨污口 截污管网 抽样监测 清淤 底泥'.split(
    ' ')
datels = ['0' + f'{i}' for i in range(1, 10)] + [f'{i}' for i in range(10, 32)]
finalls = []
for month in ['09', '10', '11', '12']:
    finalls += list(map(lambda i: '2020' + month + i, datels))
finalls = finalls[3:-22]
finalls.remove('20200931')
finalls.remove('20201131')
urldict = {}


def getarticle(page):
    content = ''
    root = etree.HTML(page.content)
    body = root.xpath("//*[@id='zhenwenzone']/div[1]/p")
    for p in body:
        content += p.text
    return content


for date in finalls:
    print(date)
    for i in range(8):
        headers = {'User-Agent': UserAgent().random}
        url = f'{base_url}/{date}/{date}_004/{date}_004_{i}.htm'
        try:
            page = httpx.get(url, headers=headers)
        except httpx.ReadTimeout:
            continue
        if page.status_code == 200:
            content = getarticle(page)
            for word in keywords:
                if word in content:
                    print(f'{word} detected')
                    urldict[f'{date}_{word}'] = url
with open('content_fzrb.json', 'w') as file:
    all_content = {}
    for key, url in urldict.items():
        headers = {'User-Agent': UserAgent().random}
        page = httpx.get(url, headers=headers)
        if page.status_code == 200:
            all_content[key] = getarticle(page)
    data = json.dumps(all_content, indent=4, separators=(
        ',', ': '), ensure_ascii=False)
    file.write(data)
print('done')
