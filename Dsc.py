import requests
import json
import threading
import pymysql.cursors
from dsc_ds import DscDatasource

db = pymysql.connect("212.64.93.216", 'root', 'yuwenque', 'dsc', charset='utf8mb4', port=3306,
                     cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()


#
# create_table_sql = '''
#     create table userinfo(id varchar(50) not null primary key ,name varchar(50),
#     os_type varchar(20),birthday varchar(50),city varchar(10), sex varchar(10),birthpet varchar(10),
#     update_time varchar(50),avatar varchar(255),education varchar(50),university varchar(50),star_sign varchar(50),ideal_mate varchar(255),
#     hometown varchar(50),height varchar(10),weight varchar (10),characters varchar (255),station varchar(100),
#     company varchar(50),hobby varchar(100),referee_id varchar(10),referee_name varchar(50) )
#     '''
#
# insert_user_sql = '''insert ignore INTO user (id,name,os_type,birthday,update_time,city,sex,birthpet,avatar,education,university,
# star_sign,ideal_mate,hometown,height,weight,characters ,station,company,hobby,referee_id,referee_name)   VALUES (
# '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') '''


# cursor.execute(create_table_sql)
class Header:
    token = "5a91dca08e54033fbf9c6ada9e25b299"
    app_version = "3.5.0"
    pass


app_version = "3.5.0"

get_user_info_url = 'https://dscapp.dscun.com/api/user/%s'
get_user_list_url = 'https://dscapp.dscun.com/api/feeds/feeds_id/%s/count/20'
get_user_list_url2 = 'https://dscapp.dscun.com/api/feeds/feeds_id/%s/count/-20'

header = Header()

ds = DscDatasource()


def insert(user):
    try:

        ds.insert(user)

        global timer
        timer = threading.Timer(3, function=get_user_info, args={user['referee_id']})
        timer.start()

    except Exception as e:
        print(e)
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
        print("开始爬取用户信息 %s" % url)
        headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; SM-N9600 Build/M1AJQ)', 'os-type': "Android",
                   'app-version': app_version, 'meet-token': header.token}
        r = requests.get(url=url, params=(), headers=headers)
        content = r.content.decode('utf-8')
        js = json.loads(content)
        data = js["data"]
        print(js)
        if js['code'] == 10003:
            newUser = login_oper("15920419761", "yuwenque")
            header.token = newUser['data']['token']
            get_user_info(id)
        else:
            if data['sex'] == 'female':
                ds.insert(data)
                # ds.update_user_time(id,data['update_time'].split(' ')[0])
    except Exception as e:
        print(e)
        pass


def update_user_list(start, count):
    query_result = ds.get_user_id_list_without_update_time(start, count)
    index = 1
    try:

        for item in query_result:
            threading.Timer(index, function=get_user_info, args={item['id']}).start()
            index = index + 1

        threading.Timer(15, function=update_user_list, args={start + 100, 100}).start()
    except Exception as e :
        print(e)


# update_user_list(1, 100)


def login_oper(name, password):
    print("重新登录")
    params = {"tel": name,
              "password": password}
    headers = {'app-version': '3.5.0', 'Content-Type': "application/json"}
    r = requests.post('https://dscapp.dscun.com/api/session', json=params, headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    return js


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

get_user_page("0")
