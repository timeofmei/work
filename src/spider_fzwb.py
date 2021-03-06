import httpx
from fake_useragent import UserAgent
from lxml import etree
'''http: // mag.fznews.com.cn/fzwb/2020/20201209/20201209_A01/20201209_A01.html
http: // mag.fznews.com.cn/fzrb/2020/20201209/20201209_001/20201209_001.html'''
base_url = "https://mag.fznews.com.cn/fzwb/2020"
datels = ['0' + f'{i}' for i in range(1, 10)] + [f'{i}' for i in range(10, 32)]
finalls = []
keywords = '黑臭 生活垃圾 内河整治 信访举报 生态环保督察 水资源保护 水域岸线管理 水污染防治 水环境治理 水生态修复 排污口 雨污口 截污管网 抽样监测 清淤 底泥'.split(
    ' ')
for month in datels[4:12]:
    finalls += list(map(lambda i: '2020' + month + i, datels))
finalls = finalls[22:226]
finalls.remove('20200631')
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
        for ban in date[:11]:
            headers = {'User-Agent': UserAgent().random}
            url = f'{base_url}/{date}/{date}_A{ban}/{date}_A{ban}_{i}.htm'
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
with open('content_fzwb.txt', 'w') as file:
    for key, url in urldict.items():
        headers = {'User-Agent': UserAgent().random}
        page = httpx.get(url, headers=headers)
        if page.status_code == 200:
            file.write(f'{key} ')
            file.write(getarticle(page))
            file.write('\n\n')
