import pymysql.cursors
from datetime import datetime

# 必须指定cursorclass，否则查询的返回结果不包含字段
db = pymysql.connect("localhost", 'root', 'yuwenque', 'keep', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
query_user_info_sql = 'select userid,birthday from keep_user'
update_user_info_sql = 'update keep_user set birthday = "%s" where userid = "%s"'
result = cursor.execute(query_user_info_sql)
result = cursor.fetchall()
# for user in result:
#     birthday = user['birthday']
#     id = user['userid']
#     try:
#         arr = birthday.split('T')
#         if len(arr) > 0:
#             birthday = arr[0]
#             print(birthday)
#             update_sql = update_user_info_sql % (birthday, id)
#             print(update_sql)
#             cursor.execute(update_sql)
#             db.commit()
#     except:
#         print(birthday)
sql = 'select userid from keep_user'
sql2= 'select * from (select author_id from keep_train) c,keep_user u where c.author_id = u.userid'
sql3 = '(select author_id from keep_train) c,(select userid from keep_user) u'

print("% %s" % 'hah')