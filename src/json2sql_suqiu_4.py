import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO jieguo (id, a, b, c, d, e, f) VALUES (%s, %s, %s, %s, %s, %s, %s )"
with open('data/content_suqiu_4.json') as file:
    data = ujson.load(file)
for i in range(len(data['序列号'])):
    data_tuple = (data['序列号'][i], data['29比较认同'][i],
                  data['29非常认同'][i], data['30比较认同'][i], data['30非常认同'][i], data['32影响较大'][i], data['32影响非常大'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
