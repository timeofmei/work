import json
import mysql.connector
from datetime import date, datetime, timedelta
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = ("INSERT INTO wb "
            "(id, keyword, 用户昵称, 微博正文, 发布时间) "
            "VALUES (%s, %s, %s, %s, %s)")
with open('content_wb.json') as file:
    data = json.load(file)
for value1 in data.values():
    for value2 in value1.values():
        data_tuple = (
            value2['id'],  value2['keyword'], value2['用户昵称'], value2['微博正文'], value2['发布时间'])
        cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
