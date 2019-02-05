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
class Header:
    token = "fd01d58be96c07a346e477adadad4716"
    app_version = "3.5.0"
    pass


app_version = "3.5.0"

get_user_info_url = 'https://dscapp.dscun.com/api/user/%s'
get_user_list_url = 'https://dscapp.dscun.com/api/feeds/feeds_id/%s/count/20'
get_user_list_url2 = 'https://dscapp.dscun.com/api/feeds/feeds_id/%s/count/-20'

header = Header()


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
        if result > 0:
            print(
                "%s , %s,%s %s(cm),%s(kg)" % (user['name'], user['birthday'], user['city'], user['height'], user['weight']))
        db.commit()
        global timer
        timer = threading.Timer(3, function=get_user_info, args={user['referee_id']})
        timer.start()

    except Exception as e:
        pass


def login(feedid):
    params = {"tel": "15920419761",
              "password": "yuwenque"}
    headers = {'app-version': app_version}
    r = requests.post('https://dscapp.dscun.com/api/session', json=params, headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)

    print("登录结果: %s" % js['msg'])
    data = js['data']
    print(data)
    tk = data['token']
    print("新token = %s" % tk)
    header.token = tk
    get_user_page(feedid)
    pass


def get_user_info(id):
    try:
        url = get_user_info_url % id
        # print("开始爬取用户信息 %s" % url)
        headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-N9600 Build/M1AJQ)', 'os-type': "Android",
                   'app-version': app_version, 'meet-token': header.token}
        r = requests.get(url=url, params=(), headers=headers)
        content = r.content.decode('utf-8')
        js = json.loads(content)
        data = js["data"]
        if data['sex'] == 'female':
            insert(data)
    except Exception as e:
        pass


def get_user_page(feedid):
    try:
        if feedid == '0':
            url = get_user_list_url % feedid
        else:
            url = get_user_list_url2 % feedid
        print("开始爬取%s" % feedid)
        headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-N9600 Build/M1AJQ)', 'os-type': "Android",
                   'app-version': app_version, 'meet-token': header.token}
        r = requests.get(url=url, params=(), headers=headers)
        content = r.content.decode('utf-8')
        js = json.loads(content)
        code = js['code']
        if code == 10003:
            print("登录失败，重新登录")
            login(feedid)
            pass
        else:
            data = js["data"]
            if len(data) > 0:
                feeds = data['feeds']
                last_feed_id = feeds[len(feeds) - 1]['feeds_id']
                for item in feeds:
                    user_id = item['user_id']
                    sex = item['sex']
                    if sex == "female":
                        global timer
                        timer = threading.Timer(3, function=get_user_info, args={user_id})
                        timer.start()
                    comment = item['comment']
                    if len(comment) > 0:
                        for c in comment:
                            if c['sex'] == 'female':
                                userId = c['user_id']
                                timer = threading.Timer(3, function=get_user_info, args={userId})
                                timer.start()
                timer = threading.Timer(5, function=get_user_page, args={last_feed_id})
                timer.start()
        pass
    except  Exception as e:
        pass


get_user_page("13104")
