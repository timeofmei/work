import ujson
import mysql.connector
skr = mysql.connector.connect(
    user="root", host="127.0.0.1", port="3306", database="work")
cursor = skr.cursor()
add_item = "INSERT INTO suqiu_new (id, 性质, 标题, 区域, 信息来源, 时间, 诉求件内容, 内容长度, 河流, 匿名or实名, 回复1, 最终回复投诉事件, 回复长度, 转处理次数, 是否黑臭) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
with open('data/result_suqiu_update.json') as file:
    data = ujson.load(file)
for i in range(1, len(data)+1):
    data_tuple = (str(i), data[str(i)]['性质'], data[str(i)]['标题'],
                  data[str(i)]['区域'], data[str(i)]['信息来源'], data[str(i)]['时间'], data[str(i)]['诉求件内容'], data[str(i)]['内容长度'], data[str(i)]['河流'], data[str(i)]['匿名or实名'], data[str(i)]['回复1'], data[str(i)]['最终回复-投诉事件'], data[str(i)]['回复长度'], data[str(i)]['转处理次数'], data[str(i)]['是否黑臭'])
    cursor.execute(add_item, data_tuple)
skr.commit()
cursor.close()
skr.close()