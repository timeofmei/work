import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO all_content_2 (id, keyword, river, district, time, source, content, name, chufa, fabu, ppp, fazhi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
with open('data/content_all_2.json') as file:
    data = ujson.load(file)
for i in range(len(data['id'])):
    data_tuple = (data['id'][i], data['keyword'][i], data['river'][i], data['district'][i],
                  data['time'][i], data['source'][i], data['content'][i], data['name'][i], data['行政管制工具（如处罚）'][i], data['信息沟通工具'][i], data['政府与私人合作（ppp）'][i], data['法制工具（修订法规）'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
