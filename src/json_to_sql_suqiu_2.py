import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO guifan (id, guifan) VALUES (%s, %s )"
with open('data/content_suqiu_2.json') as file:
    data = ujson.load(file)
for i in range(len(data['id'])):
    data_tuple = (data['id'][i], data['guifan'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
