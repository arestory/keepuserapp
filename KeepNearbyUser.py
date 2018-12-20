import requests
import json
import threading

import pymysql.cursors

import warnings

warnings.filterwarnings('ignore')

db = pymysql.connect("localhost", 'root', 'yuwenque', 'keep', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
# 22.7964393209,113.4228515625 广州
mLat = 29.505631282400714
mLng = 110.35738281250194
# https://api.gotokeep.com/social/v4/geo/nearby/people?lat=22.709620939085166&lon=113.80505583018066
insert_user_sql = '''INSERT ignore INTO KEEP_USER_INFO (userid,name,birthday,country,province,city,district,gender,jointime,nationCode,citycode,bio,avatar,totalDuration,runningDistance,weight,bmi)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''

insert_train_sql = '''INSERT ignore  INTO KEEP_TRAIN (item_id,author_id,author_name,content,tags,latitude,longitude,images,created,photo)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''

query_user_sql = '''

select birthday,country,city,joinTime,nationCode,citycode,province from keep_user where userid ='%s' limit 1
'''


# 38.916299186200895&lon=112.43929687499804
# 39.3002991862,116.2792968750 北京
#
# 26.9024768863,98.7890625000 云南
class Total:
    count = 0
    lastDownload = 0


total = Total()


def testQuery(userid):
    cursor.execute(query_user_sql % userid)
    olduser = cursor.fetchone()
    birthday = olduser['birthday']
    country = olduser['country']
    city = olduser['city']
    joinTime = olduser['joinTime']
    nationCode = olduser['nationCode']
    citycode = olduser['citycode']
    province = olduser['province']
    pass


# testQuery('54ec192be5210a3641b39aaa')


def insert_user(keepuser):
    try:
        db.ping(reconnect=True)
        userid = keepuser.get('_id')
        cursor.execute(query_user_sql % userid)
        olduser = cursor.fetchone()
        if olduser:
            birthday = olduser['birthday']
            if len(birthday) == 0 or birthday == 'None':
                birthday = keepuser.get('birthday')
            country = olduser['country']
            if country == '' or country == 'None':
                country = keepuser.get('country')
            city = olduser['city']
            if city == '' or city == 'None':
                city = keepuser.get('city')
            joinTime = olduser['joinTime']
            if joinTime == '' or joinTime == 'None':
                joinTime = keepuser.get('joinTime')
            nationCode = olduser['nationCode']
            if nationCode == '' or nationCode == 'None':
                nationCode = keepuser.get('nationCode')
            citycode = olduser['citycode']
            if citycode == '' or citycode == 'None':
                citycode = keepuser.get('citycode')
            province = olduser['province']
            if province == '' or province == 'None':
                province = keepuser.get('province')
        else:
            birthday = keepuser.get('birthday')
            country = keepuser.get('country')
            city = keepuser.get('city')
            joinTime = keepuser.get('joinTime')
            nationCode = keepuser.get('nationCode')
            citycode = keepuser.get('citycode')
            province = keepuser.get('province')

        oldrecord = ''
        # print("insertdata,", keepuser.get('username'))
        data = (keepuser.get('_id'), keepuser.get('username'), birthday, country,
                province,
                city, keepuser.get('district'), keepuser.get('gender'),
                joinTime,
                nationCode, citycode, keepuser.get('bio').replace("'", "—"),
                keepuser.get('avatar'), keepuser.get('totalDuration'), keepuser.get('runningDistance'),
                keepuser.get('weight'), keepuser.get('bmi'))
        result = cursor.execute(insert_user_sql % data)
        db.commit()
        total.count = total.count + result
        if result == 1:
            print("插入一条新用户数据")

    except Exception as e:
        print(e)
    # getUserEntries(keepuser.get('_id'),"")


import random


def createRandomLatLng():
    mRandomLat = random.uniform(4, 53)
    mRandomLng = random.uniform(73, 135)
    return mRandomLat, mRandomLng


lastDownload = 0


def try_get_geo_user(lat, lng):
    try:
        url = 'https://api.gotokeep.com/social/v4/geo/nearby/people?lat=%s&lon=%s' % (lat, lng)
        r = requests.get(url)
        content = r.content.decode('utf-8')
        print(url)
        # print(content)
        data = json.loads(content)
        users = data['data']['users']

        index = 0
        for user in users:
            index = index + 1
            # print(user['user'])

            item = user['user']
            userProfile = user['userProfile']
            item['totalDuration'] = userProfile.get('totalDuration')
            item['runningDistance'] = userProfile.get('runningDistance')
            item['weight'] = userProfile.get('weight')
            item['bmi'] = userProfile.get('bmi')

            insert_user(item)
            # threading.Timer(15, function=getUserEntries, args=[user['user']['_id'],""]).start()

        if total.count < 10000:
            # time.sleep(2)

            if total.count != total.lastDownload:
                print("已下载 %s" % total.count)
                total.lastDownload = total.count
                pass
            latlng = createRandomLatLng()
            lat = latlng[0]
            lng = latlng[1]
            threading.Timer(3, function=try_get_geo_user, args=[lat, lng]).start()
            pass
    except Exception as e:
        pass
    pass


latlng = createRandomLatLng()
lat = latlng[0]
lng = latlng[1]

try_get_geo_user(lat, lng)


class Train:
    pass


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
