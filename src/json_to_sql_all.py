import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO all_content (id, keyword, river, district, time, source, content, name, chufa, fabu, ppp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
with open('data/content_all.json') as file:
    data = ujson.load(file)
for i in range(len(data['id'])):
    data_tuple = (data['id'][i], data['keywords'][i], data['rivers'][i], data['districts'][i],
                  data['times'][i], data['sources'][i], data['articles'][i], data['names'][i], data['政府治理-行政处罚'][i], data['政府治理-信息发布'][i], data['政府治理-PPP'][i])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()
