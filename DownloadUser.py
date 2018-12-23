import pymysql.cursors, time
import download,os

db = pymysql.connect("localhost", 'root', 'yuwenque', 'keep', charset='utf8mb4')
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

sql ='''
select avatar,gender,userid from keep_user_info where gender ='F' and birthday like '199%' or birthday like '200%' or birthday like '201%' limit 5001,10000 
'''
path = '/Users/yuwenque/Downloads/keepuser/'


cursor.execute(sql)
list = cursor.fetchall()
for i in range(0, len(list)):
    item = list[i]
    photo_name = path + item['gender'] + "/" + item['userid'] + ".jpg"
    if i % 10 == 0 and i != 0:
        time.sleep(10)
    try:
        if not os.path.exists(photo_name):
            try:
                download.download_file(item['avatar'], photo_name)
            except Exception as e2:
                os.remove(photo_name)
                print(e2)

            time.sleep(3)
    except Exception as e:
        print(e)
