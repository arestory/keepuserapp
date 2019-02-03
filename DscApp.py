import requests
import json
import threading

import pymysql.cursors

db = pymysql.connect("212.64.93.216", 'root', 'yuwenque', 'dsc', charset='utf8mb4', port=3306,
                     cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

create_table_sql = '''

    create table user(id varchar(50) not null primary key ,name varchar(50),
    os_type varchar(20),birthday varchar(50),city varchar(10), sex varchar(10),birthpet varchar(10), 
    avatar varchar(255),education varchar(50),university varchar(50),star_sign varchar(50),ideal_mate varchar(255), 
    hometown varchar(50),height varchar(10),weight varchar (10),characters varchar (255),station varchar(100),
    company varchar(50),hobby varchar(100),referee_id varchar(10),referee_name varchar(50) )
    '''

insert_user_sql = '''insert ignore INTO user (id,name,os_type,birthday,city,sex,birthpet,avatar,education,university,
star_sign,ideal_mate,hometown,height,weight,characters ,station,company,hobby,referee_id,referee_name)   VALUES (
'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') '''

# cursor.execute(create_table_sql)

token = "6f0d547bbae230068d98e778f24f3126"
app_version = "3.5.0"

get_user_info_url = 'https://dscapp.dscun.com/api/user/%s'
get_user_list_url = 'https://dscapp.dscun.com/api/feeds/feeds_id/%s/count/10'


def insert(user):
    try:

        db.ping(reconnect=True)

        sql = insert_user_sql % (
            user['id'], user['name'], user['os_type'], user['birthday'], user['city'], user['sex'], user['birthpet'],
            user['avatar'], user['education'], user['university'], user['star_sign'], user['ideal_mate'],
            user['hometown'],
            user['height'],
            user['weight'], user['characters'], user['station'], user['company'], user['hobby'], user['referee_id'],
            user['referee_name'])
        result = cursor.execute(sql)
        print("插入一个新用户：%s %s" % (user['name'],result))
        db.commit()

    except Exception as e:
        pass


def get_user_info(id):
    url = get_user_info_url % id
    print("开始爬取用户信息 %s" % url)
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-N9600 Build/M1AJQ)', 'os-type': "Android",
               'app-version': app_version, 'meet-token': token}
    r = requests.get(url=url, params=(), headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    data = js["data"]
    insert(data)


def get_user_page(feedid):
    url = get_user_list_url % feedid
    print("开始爬取%s" % feedid)
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-N9600 Build/M1AJQ)', 'os-type': "Android",
               'app-version': app_version, 'meet-token': token}
    r = requests.get(url=url, params=(), headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    data = js["data"]
    last_feed_id = data['rem_feeds']
    last_feed_id = last_feed_id[len(last_feed_id) - 1]
    print(data)
    feeds = data['feeds']
    for item in feeds:
        user_id = item['user_id']
        sex =item['sex']
        if sex == "female":
            threading.Timer(3, function=get_user_info, args={user_id}).start()

        pass
    threading.Timer(5, function=get_user_page, args={last_feed_id}).start()
    pass


get_user_page("0")
