import json
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO dnw (id, keyword, biaoti, time, jianjie, link, article) VALUES (%s, %s, %s, %s, %s, %s, %s)"
with open('content_dnw.json') as file:
    data = json.load(file)
for keyword, value1 in data.items():
    for value2 in value1.values():
        data_tuple = (value2['id'], keyword, value2['biaoti'], value2['time'],
                      value2['jianjie'], value2['link'], value2['article'])
        cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
