import pandas as pd
import math
import ujson
import jieba
jieba.initialize()
data = pd.read_excel('../data/新诉求数据.xlsx')
headers = ['序列号', '标题', '投诉件内容', '回复1']

trusts_highs = ['请', '尽快', '恳请', '协商', '支持', '希望', '处理', '扰民', '违法',
                '法制', '恶劣', '违反', '严重影响', '及时', '制止', '方案', '查处', '调查', '重视']
trusts_mediums = [
    '公众利益', '政府', '公信力', '媒体', '监督', '纠正', '杜绝', '不良行为', '相信', '下决心', '怀疑', '建议', '投诉', '答复', '谢谢', '帮助', '复制', '黏贴']
trusts_lows = ['无法完工', '迟迟', '等', '进度', '恢复',  '导致', '扰民', '解决', '改造',
               '关心', '真正', '至少', '为什么', '得不到解决', '意义', '无能', '效率', '所谓']
tools_xingzheng = ['整治', '启动', '巡查', '列入', '改善', '清淤', '截污', '动工',
                   '完成', '处置', '依法', '责令', '整改', '经查',  '行动',  '监管',  '严令',  '禁止']
tools_xinxi = ['约谈',  '避免',  '敬请谅解',   '谢谢',  '不便',  '好转',  '尽快',  '电话',  '暂未',  '经查',  '加强',
               '感谢',  '关注',  '理解',  '下达',  '任务',  '支持',   '实施',  '缓解',   '预计',   '落实',  '烦请',  '反映',  '热心']
tools_hezuo = ['PPP',  '恢复',  '深表歉意',  '市民',  '设计单位',  '协调',
               '督促',  '要求',  '尽量',   '方案',  '积极',   '联系',  '跟踪',  '告知']
tools_fazhi = ['违规', '制止', '调查', '印发', '规定', '严格', '执法', '依法查处']
all_content = {}
for header in headers:
    all_content[header] = list(data[header])
all_content['trust'] = []
all_content['tool'] = []
all_content['tool_xingzheng_cipin'] = []
all_content['tool_xingzheng_bizhong'] = []
all_content['tool_xinxi_cipin'] = []
all_content['tool_xinxi_bizhong'] = []
all_content['tool_hezuo_cipin'] = []
all_content['tool_hezuo_bizhong'] = []
all_content['tool_fazhi_cipin'] = []
all_content['tool_fazhi_bizhong'] = []
for i in range(len(all_content['序列号'])):
    ks = [0, 0, 0, 0]
    bizhongs = [0, 0, 0, 0]
    tools = ['xingzheng', 'xinxi', 'hezuo', 'fazhi']
    content_str = all_content['投诉件内容'][i]
    reply_str = all_content['回复1'][i]
    reply_word_num = len(jieba.lcut(reply_str))
    trust = 0.5
    mid_num = 0
    for high in trusts_highs:
        if high in content_str:
            trust *= 1.1
    for low in trusts_lows:
        if low in content_str:
            trust /= 1.1
    for mid in trusts_mediums:
        if mid in content_str:
            mid_num += 1
    if trust > 0.5:
        temp = (trust - 0.5) * 0.1 * mid_num
        trust -= temp
    elif trust < 0.5:
        temp = (0.5 - trust) * 0.1 * mid_num
        trust += temp
    yiwen_num = content_str.count(
        '？') + content_str.count('?')
    gantan_num = content_str.count(
        '！') + content_str.count('!')
    if yiwen_num > 2 or gantan_num > 2:
        trust *= 1 / math.exp(yiwen_num + gantan_num)
    if trust < 0:
        trust = 0
    elif trust > 1:
        trust = 1
    all_content['trust'].append(trust)

    for xingzheng in tools_xingzheng:
        if xingzheng in reply_str:
            ks[0] += 1
    all_content['tool_xingzheng_cipin'].append(ks[0])
    bizhongs[0] = ks[0] * 100 / reply_word_num
    all_content['tool_xingzheng_bizhong'].append(f"{bizhongs[0]}%")
    for xinxi in tools_xinxi:
        if xinxi in reply_str:
            ks[1] += 1
    all_content['tool_xinxi_cipin'].append(ks[1])
    bizhongs[1] = ks[1] * 100 / reply_word_num
    all_content['tool_xinxi_bizhong'].append(f"{bizhongs[1]}%")
    for hezuo in tools_hezuo:
        if hezuo in reply_str:
            ks[2] += 1
    all_content['tool_hezuo_cipin'].append(ks[2])
    bizhongs[2] = ks[2] * 100 / reply_word_num
    all_content['tool_hezuo_bizhong'].append(f"{bizhongs[2]}%")
    for fazhi in tools_fazhi:
        if fazhi in reply_str:
            ks[3] += 1
    all_content['tool_fazhi_cipin'].append(ks[3])
    bizhongs[3] = ks[3] * 100 / reply_word_num
    all_content['tool_fazhi_bizhong'].append(f"{bizhongs[3]}%")
    if max(ks) > 0:
        if bizhongs.count(max(bizhongs)) == 1:
            all_content['tool'].append(tools[bizhongs.index(max(bizhongs))])
        else:
            all_content['tool'].append('')
            for idx in range(4):
                if ks[idx] == max(ks):
                    all_content['tool'][i] += f'{tools[idx]} '
    else:
        all_content['tool'].append('none')

with open('some.json', 'w') as file:
    json_data = ujson.dumps(all_content, indent=4, ensure_ascii=False)
    file.write(json_data)
