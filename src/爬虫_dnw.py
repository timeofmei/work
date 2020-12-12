import httpx
import json
from fake_useragent import UserAgent
from lxml import etree
import re
import time
base_url = 'http://search.fjsen.com/search.php?q='
keywords = '黑臭 生活垃圾 内河整治 信访举报 生态环保督察 水资源保护 水域岸线管理 水污染防治 水环境治理 水生态修复 排污口 雨污口 截污管网 抽样监测 清淤 底泥'.split(
    ' ')
all_content = {}
i = 0
for keyword in keywords:
    print(keyword)
    all_content[f'{keyword}'] = {}
    url = f'{base_url}{keyword} 福州&o=default&p='
    for p in range(1, 501):
        print(p)
        url = f'{url}{p}'
        headers = {'User-Agent': UserAgent().random}
        try:
            page = httpx.get(url, headers=headers)
        except:
            continue
        if page.status_code == 200:
            root = etree.HTML(page.content)
            titles = root.xpath("//div[@class='data-list']")
            for title in titles:
                content = {}
                content['biaoti'] = ''.join(title.xpath(
                    "./h2/a/text()|./h2/a/em/text()"))
                try:
                    m = all_content[keyword][content['biaoti']]
                    continue
                except KeyError:
                    i += 1
                content['id'] = i
                content['time'] = re.search(
                    '[0-9]+-[0-9]+-[0-9]+', title.xpath("./h2/text()")[1]).group()
                content['jianjie'] = ''.join(title.xpath(
                    "./div[1]/p[1]/text()|./div[1]/p[1]/em/text()"))
                content['link'] = title.xpath(
                    "./div[1]/p[2]/a[1]/@href")[0]
                try:
                    detail_page = httpx.get(content['link'], headers=headers)
                    if detail_page.status_code == 200:
                        print("OK")
                        root_detail = etree.HTML(detail_page.content)
                        article = '\n'.join(root.xpath(
                            "//p/text()|//p/strong/text()"))
                        article = article.replace('\n', '')
                        article = article.replace('\t', '')
                        content['article'] = article
                    else:
                        content['article'] = content['biaoti']
                except:
                    content['article'] = content['biaoti']

                all_content[keyword][content['biaoti']] = content


with open('content_dnw.json', 'w') as file:
    data = json.dumps(all_content, indent=4, separators=(
        ',', ': '), ensure_ascii=False)
    file.write(data)
print("done")
