import httpx
import ujson
import re
from lxml.etree import HTML
import datetime
url = "http://fz12345.fuzhou.gov.cn/fzwp/webCallSearch/search?q=1&keyWord=黑臭&selectId=1&eCreateTime=2016-12-31"
baseUrl = "http://fz12345.fuzhou.gov.cn"
suqius = {}
rivers = ['龙津河', '洪阵河', '文藻河', '洋里溪', '新透河', '琴亭河', '浦上河', '光明港二支河', '陈厝河', '三捷河', '泮洋河', '竹屿河', '君竹河', '茶园河', '红星河', '飞凤河', '淌洋河', '金港河', '打铁港', '大庆河', '台屿河', '磨洋河', '浦东河', '洋下河', '君竹', '瀛洲河', '达道河', '梅峰河', '潘墩河', '河流', '跃进河', '济南河', '牛浦河', '马洲支河', '阳岐河', '东郊河', '吴山河', '白湖亭河', '竹榄河', '半洋亭河']
id = 0
for i in range(1, 23):
    data = {
        "cp": str(i),
        "type": ""
    }
    resp = httpx.post(url=url, data=data)
    if resp.status_code != 200:
        continue
    page = HTML(resp.text)
    resultLs = page.xpath("//div[@class='search_list']/ul/li")
    for result in resultLs:
        id += 1
        print(id)
        suqius[id] = {}
        suqius[id]['id'] = id
        suqius[id]['性质'] = result.xpath("./div[1]/a/text()")[0][1:3]
        suqius[id]['标题'] = result.xpath("./div[1]/a/text()")[0][4:].strip()
        suqius[id]['区域'] = result.xpath("./div[2]/p[2]/span[2]/text()")[0][result.xpath("./div[2]/p[2]/span[2]/text()")[0].index("：")+1:]
        suqius[id]['信息来源'] = result.xpath("./div[2]/p[2]/span[4]/text()")[0][result.xpath("./div[2]/p[2]/span[4]/text()")[0].index("：")+1:]
        suqiuTimeStr = result.xpath("./div[2]/p[2]/span[5]/text()")[0][result.xpath("./div[2]/p[2]/span[5]/text()")[0].index("：")+1:]
        suqiuTime = datetime.datetime(int(suqiuTimeStr.split("-")[0]), int(suqiuTimeStr.split("-")[1]), int(suqiuTimeStr.split("-")[2]))
        suqius[id]['时间'] = suqiuTime.strftime(r"%m/%d/%Y")


        resultUrl = baseUrl + result.xpath("./div[1]/a/@href")[0]
        resultResp = httpx.get(url=resultUrl)
        if resultResp.status_code != 200:
            continue
        resultPage = HTML(resultResp.text)
        suqius[id]['诉求件内容'] = resultPage.xpath("//div[@class='table']/table/tr[3]/td[2]/p/text()")[0].strip()
        suqius[id]['内容长度'] = len(suqius[i]['诉求件内容'])
        suqius[id]['河流'] = ""
        for river in rivers:
            if river in suqius[id]['诉求件内容'] or river in suqius[id]['标题'] or river in resultPage.xpath("//div[@class='table']/table/tr[7]/td[2]/p/text()")[0]:
                suqius[id]['河流'] += f"{river} "
        if suqius[id]['河流'] == "":
            suqius[id]['河流'] = "无"
        else:
            suqius[id]['河流'] = suqius[id]['河流'].strip()
        if resultPage.xpath("//div[@class='table']/table/tr[4]/td[1]/text()")[0] == "诉求附件":
            suqius[id]['匿名or实名'] = resultPage.xpath("//div[@class='table']/table/tr[7]/td[2]/p/text()")[0]
            replyContent = resultPage.xpath("//div[@class='table']/table/tr[6]/td[2]//text()")
            
        else:
            suqius[id]['匿名or实名'] = resultPage.xpath("//div[@class='table']/table/tr[6]/td[2]/p/text()")[0]
            replyContent = resultPage.xpath("//div[@class='table']/table/tr[5]/td[2]//text()")
        if len(replyContent) == 1:
            suqius[id]["回复1"] = "无"
            suqius[id]["最终回复-投诉事件"] = 0
        else:
            some = -4
            try:
                suqius[id]["回复1"] = replyContent[some].strip()
            except:
                some += 1
                suqius[id]["回复1"] = replyContent[some].strip()
            if "nbsp" in suqius[id]["回复1"]:
                suqius[id]["回复1"] = replyContent[some - 1].strip()
            replyTimeStr = re.compile(r"\d{4}-\d{2}-\d{2}").search(replyContent[-2]).group()
            replyTime = datetime.datetime(int(replyTimeStr.split("-")[0]), int(replyTimeStr.split("-")[1]), int(replyTimeStr.split("-")[2]))
            suqius[id]["最终回复-投诉事件"] = int(replyTime.__sub__(suqiuTime).days)
        suqius[id]["回复长度"] = len(suqius[id]["回复1"])
        if suqius[id]["回复长度"] <= 5:
            suqius[id]["回复1"] = "无"
            suqius[id]["回复长度"] = 1
        suqius[id]["转处理次数"] = int((len(replyContent) - 1) / 2)

with open("../data/result_suqiu.json", "w") as f:
    f.write(ujson.dumps(suqius, ensure_ascii=False))
    print("done")