import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO jieguo (a29, b30, c32, scores) VALUES (%s, %s, %s, %s)"
with open('data/content_suqiu_5.json') as file:
    data = ujson.load(file)
for i in range(len(data['结果认同-29'])):
    data_tuple = (data['结果认同-29'][i], data['结果认同-30'][i],
                  data['结果认同-32'][i], data['scores'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
