import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO guifan (id, liji, lita, shengtai) VALUES (%s, %s, %s, %s)"
with open('../data/content_suqiu_6.json') as file:
    data = ujson.load(file)
for i in range(len(data['values'])):
    data_tuple = (i, data['values'][str(i)]['lijis'], data['values'][str(i)]['litas'],
                  data['values'][str(i)]['shengtais'])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
