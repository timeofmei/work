import httpx
import ujson
import re
from lxml.etree import HTML
import datetime
url = "http://fz12345.fuzhou.gov.cn/fzwp/webCallSearch/search?q=1&keyWord=黑臭&selectId=1&eCreateTime=2016-12-31"
baseUrl = "http://fz12345.fuzhou.gov.cn"
suqius = {}
ids = [1, 2, 3, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 118, 119, 120, 121, 122, 123, 124, 126, 127, 128, 129, 130, 131, 133, 134, 135, 136, 138, 139, 140, 141, 142, 143, 146, 147, 149, 150, 151, 157, 158, 160, 161, 162, 163, 164, 165, 166, 168, 169, 170, 172, 173, 175, 176, 177, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 197, 199, 200, 201, 203, 204, 205, 206, 207, 208, 210, 211, 213, 214, 215, 216, 217, 218, 219, 220, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 244, 245, 246, 247, 249, 250, 251, 252, 253, 254, 255, 256, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 273, 274, 275, 276, 277, 278, 279, 280, 281, 283, 284, 286, 287, 292, 294, 295, 297, 298, 299, 300, 303, 306, 308, 309, 310, 311, 313, 314, 315, 316, 48, 49, 87]
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
        suqius[id]['诉求件内容'] = "".join(resultPage.xpath("//div[@class='table']/table/tr[3]/td[2]/p//text()")).strip()
        suqius[id]['内容长度'] = len(suqius[id]['诉求件内容'])
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
            replyContent = resultPage.xpath("//div[@class='table']/table/tr[6]/td[2]")[0]
        else:
            suqius[id]['匿名or实名'] = resultPage.xpath("//div[@class='table']/table/tr[6]/td[2]/p/text()")[0]
            replyContent = resultPage.xpath("//div[@class='table']/table/tr[5]/td[2]")[0]

        if len(replyContent) == 0:
            suqius[id]["回复1"] = "无"
            suqius[id]["最终回复-投诉事件"] = 0
        else:
            suqius[id]["回复1"] = "".join(replyContent.xpath("./text()")).replace(" ", "")
            
            replyTimeStr = re.compile(r"\d{4}-\d{2}-\d{2}").search(replyContent.xpath("./span//text()")[-1]).group()
            replyTime = datetime.datetime(int(replyTimeStr.split("-")[0]), int(replyTimeStr.split("-")[1]), int(replyTimeStr.split("-")[2]))
            suqius[id]["最终回复-投诉事件"] = int(replyTime.__sub__(suqiuTime).days)
        suqius[id]["回复长度"] = len(suqius[id]["回复1"])
        if suqius[id]["回复长度"] <= 5:
            suqius[id]["回复1"] = "无"
            suqius[id]["回复长度"] = 1
        suqius[id]["转处理次数"] = int((len(replyContent) - 1) / 2)

        if id not in ids:
            suqius[id]["是否黑臭"] = "no"
        else:
            suqius[id]["是否黑臭"] = "yes"

with open("../data/result_suqiu_update.json", "w") as f:
    f.write(ujson.dumps(suqius, ensure_ascii=False))
    print("done")