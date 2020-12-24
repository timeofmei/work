import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO suqiu (id, 标题, 诉求件内容, 回复1, trust, tool, tool_xingzheng_cipin, tool_xingzheng_bizhong, tool_xinxi_cipin, tool_xinxi_bizhong, tool_hezuo_cipin, tool_hezuo_bizhong, tool_fazhi_cipin, tool_fazhi_bizhong) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
with open('data/content_suqiu.json') as file:
    data = ujson.load(file)
for i in range(len(data['id'])):
    data_tuple = (data['id'][i], data['标题'][i], data['投诉件内容'][i], data['回复1'][i],
                  data['trust'][i], data['tool'][i], data['tool_xingzheng_cipin'][i], data['tool_xingzheng_bizhong'][i], data['tool_xinxi_cipin'][i], data['tool_xinxi_bizhong'][i], data['tool_hezuo_cipin'][i], data['tool_hezuo_bizhong'][i], data['tool_fazhi_cipin'][i], data['tool_fazhi_bizhong'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
