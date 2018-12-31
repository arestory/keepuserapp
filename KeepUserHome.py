# coding=UTF-8
import pymysql.cursors
import json
import requests
import threading
import warnings

import time

warnings.filterwarnings('ignore')
user_home_url = 'https://api.gotokeep.com/social/v5/people/home/?userId=%s'
insert_train_sql = '''INSERT ignore  INTO KEEP_TRAIN (item_id,author_id,author_name,content,tags,latitude,longitude,images,created,photo)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''

query_userid_list_sql = 'select userid from keep_user_info order by joinTime limit %s,%s'
db = pymysql.connect("localhost", 'root', 'yuwenque', 'keep', charset='utf8mb4', port=3306,cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

update_user_info_sql = 'UPDATE keep_user_info SET birthday = "%s",country ="%s",city="%s",joinTime="%s",nationCode="%s",citycode="%s",province="%s" WHERE userid = "%s"'
query_userid__None_birthday_list_sql = 'select userid from keep_user_info where birthday ="None" or length(birthday)=0 limit "%s","%s"'

query_birthday = '''

select t.bd,count(*) from (select left(birthday,4) as bd from keep_user where birthday not like '1900%' and birthday not like '201%'  and birthday != 'None') as t group by t.bd;
'''


class Train:
    pass


def rigthBirthday():
    sql = 'select birthday ,userid  from keep_user where length(birthday)>0'
    updateSql = 'UPDATE keep_user SET birthday = "%s" where userid ="%s"'
    cursor.execute(sql)
    results = cursor.fetchall()
    try:
        for item in results:
            userid = item['userid']
            birthday = item['birthday'].split("T")[0]
            cursor.execute(updateSql % (birthday, userid))
            db.commit()
    except Exception as e:
        pass


# rigthBirthday()

def getUserInfo(userid):
    try:
        r = requests.get(
            user_home_url % userid)
        content = r.content.decode('utf-8')
        js = json.loads(content)
        headInfo = js['data']['headInfos']
        birthday = headInfo['birthday']
        birthday = birthday.split("T")[0]
        country = headInfo['country']
        city = headInfo['city']
        joinTime = headInfo['joinTime']
        nationCode = headInfo['nationCode']
        citycode = headInfo['citycode']
        province = headInfo['province']
        db.ping(reconnect=True)

        value = (birthday, country, city, joinTime, nationCode, citycode, province, userid)
        result = cursor.execute(update_user_info_sql % value)
        db.commit()
        if result == 1:
            print("已更新 " + userid + " 用户")
    except Exception as e:
        pass




def updateUser(start,end):
    cursor.execute(query_userid__None_birthday_list_sql % (start,end))
    userIdList = cursor.fetchall()
    print("有%s用户没有生日" % len(userIdList))
    index = 1
    for userid in userIdList:
        getUserInfo(userid['userid'])
        time.sleep(2)
        pass
    updateUser(end+1,end+100)

# updateUser(0,100)


# for userid in up-map-div


def getUserEntries(userId, lastId):
    r = requests.get(
        "https://api.gotokeep.com/social/v5/people/listmodule?userId=" + userId + "&module=entry&lastId=" + lastId)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    data = js["data"]
    if data.get('info'):
        items = data['info']
        for item in items:
            train = Train()
            train.id = item["_id"]
            train.author_id = item['author']["_id"]
            train.author_name = item['author']["username"]
            train.content = item["content"]
            tags = item['hashTags']
            tags_str = ""
            if len(tags) > 0:
                for tag in tags:
                    tags_str = tags_str + tag + ","
            train.tags = tags_str

            geo = item['geo']
            if len(geo) > 0:
                train.latitude = geo[0]
                train.longitude = geo[1]
            train.longitude = ''
            train.latitude = ''
            if len(geo) == 2:
                train.longitude = geo[0]
                train.latitude = geo[1]
            imgs_str = ''
            try:
                images = item['images']
                if len(images) > 0:
                    for img in images:
                        imgs_str = img + "," + imgs_str

                train.photo = item['photo']
            except Exception as e:
                pass
            train.created = item['created']

            train.images = imgs_str

            insert_train(train)

        newLastId = js['data']['lastId']
        threading.Timer(20, function=getUserEntries, args=[userId, newLastId]).start()
    else:
        print(userId + "的列表已爬取完毕")


def insert_train(train):
    try:
        db.ping(reconnect=True)

        data = (
            train.id, train.author_id, train.author_name, train.content.replace("'", "—"), train.tags, train.latitude,
            train.longitude,
            train.images, train.created, train.photo)
        result = cursor.execute(insert_train_sql % data)
        if result > 0:
            print("insert_train插入结果：", result)

        db.commit()
    except Exception as e:
        # print(e)
        pass


cursor.execute("select count(1) as total from keep_user_info order by joinTime")
total = cursor.fetchone()['total']
print("total = %s" % total)


def query(start, end):
    print("开始查询 %s-%s" % (start, end))
    if end >= total:
        print("查询完毕")
        return
    cursor.execute(query_userid_list_sql % (start, end))
    userids = cursor.fetchall()
    index = -1
    for userid in userids:
        id = userid['userid']
        print("正在查询" + userid['userid']+",当前页数："+start)
        getUserEntries(id, "")
        if index % 3 == 0:
            time.sleep(5)
        index = index + 1
    query(end + 1, end + 1000)

query(1, 1000)
