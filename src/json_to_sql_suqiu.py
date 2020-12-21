import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO suqiu (id, 标题, 诉求件内容, 回复1, trust, tool_xingzheng, tool_xinxi, tool_hezuo, tool_fazhi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
with open('data/content_suqiu.json') as file:
    data = ujson.load(file)
for i in range(len(data['id'])):
    data_tuple = (data['id'][i], data['标题'][i], data['投诉件内容'][i], data['回复1'][i],
                  data['trust'][i], data['tool_xingzheng'][i], data['tool_xinxi'][i], data['tool_hezuo'][i], data['tool_fazhi'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
