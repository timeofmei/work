import mysql.connector
import ujson
import datetime

skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO liuyan (id, forumName, subject, domainName, stateInfo, content, dateline) VALUES (%s, %s, %s, %s, %s, %s, %s)"
for i in range(1, 7):
    with open(f'data/df{i}.json') as file:
        data = ujson.load(file)['resultData']['data']
        for j in range(len(data)):
            block = data[j]
            block['dateline'] = datetime.datetime.fromtimestamp(
                block['dateline'])
            data_tuple = (block['tid'], block['forumName'], block['subject'],
                          block['domainName'], block['stateInfo'], block['content'], block['dateline'])
            cursor.execute(add_item, data_tuple)


skr.commit()
cursor.close()
skr.close()
