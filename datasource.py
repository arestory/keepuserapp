# coding=UTF-8
import pymysql.cursors

import time, datetime
import numpy
import requests
import threading
import json


class Train:
    pass


class UserDatasource(object):
    # 必须指定self.cursorclass，否则查询的返回结果不包含字段
    db = pymysql.connect("212.64.93.216", 'root', 'yuwenque', 'keep', charset='utf8mb4', port=3306,
                         cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()

    birthday_sql = '''
    select t.bd ,count(*) as count from (
                select cast(left(birthday,4) as SIGNED INTEGER) as bd FROM keep_user_info 
                where birthday NOT LIKE '1900%%' and birthday != 'None' and birthday not like '201%%' ) 
              as t group by t.bd
    '''

    birthday_of_province_sql = '''
    select t.bd ,count(*) as count from (
                select cast(left(birthday,4) as SIGNED INTEGER) as bd FROM keep_user_info 
                where province='%s' and birthday NOT LIKE '1900%%' and birthday != 'None' and birthday not like '201%%' ) 
              as t group by t.bd
    '''

    birthday_of_city_sql = '''
    select t.bd ,count(*) as count from (
                select cast(left(birthday,4) as SIGNED INTEGER) as bd FROM keep_user_info 
                where city like '%s%%' and birthday NOT LIKE '1900%%' and birthday != 'None' and birthday not like '201%%' ) 
              as t group by t.bd
    '''

    province_city_user_sql = ' select t.count,t.city from ( select count(*) as count ,city from keep_user_info where province Like "%s%%" group by city) as t'
    all_city_user_sql = '''
            select t.count,t.city from ( select count(*) as count ,city from keep_user_info where country='中国' group by city) as t
    '''

    country_user_bmi_sql = 'select t.bmi,t.count from ( select count(1) as count ,bmi from keep_user_info group by bmi) as t'
    query_user_timerange_sql = 'select count(*) as count from keep_user_info where joinTime>=%s   and joinTime<%s'

    count_user_duration_sql = 'select * from(select count(*) as count,totalDuration as duration from keep_user_info where totalDuration !="None" and totalDuration>0 group by totalDuration) t order by t.duration desc;'

    insert_user_sql = '''INSERT ignore INTO keep_user_info (userid,name,birthday,country,province,city,district,gender,jointime,nationCode,citycode,bio,avatar,totalDuration,runningDistance,weight,bmi)
                    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''

    query_user_sql = '''

    select birthday,country,city,joinTime,nationCode,citycode,province from KEEP_USER_INFO where userid ='%s' limit 1
    '''

    insert_train_sql = '''INSERT ignore  INTO KEEP_TRAIN (item_id,author_id,author_name,content,tags,latitude,longitude,images,created,photo)
                     VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''

    def getUserEntries(self, userId, lastId):
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

                self.insert_train(train)

            newLastId = js['data']['lastId']
            threading.Timer(10, function=self.getUserEntries, args=[userId, newLastId]).start()
        else:
            print(userId + "的列表已爬取完毕")

    def getUserEntryList(self, userId, lastId=""):
        url = "https://api.gotokeep.com/social/v5/people/listmodule?userId=" + userId + "&module=entry"
        if len(lastId) > 0:
            url = "https://api.gotokeep.com/social/v5/people/listmodule?userId=" + userId + "&module=entry&lastId=" + lastId

        r = requests.get(
            url)
        content = r.content.decode('utf-8')
        js = json.loads(content)
        result = []
        data = js["data"]
        if data.get('info'):
            items = data['info']
            for item in items:
                train = {'id': item["_id"], 'author_id': item['author']["_id"],
                         'author_name': item['author']["username"], 'content': item["content"]}
                tags = item['hashTags']

                trainItem = Train()
                trainItem.id = train['id']
                trainItem.author_id = train['author_id']
                trainItem.author_name = train['author_name']
                trainItem.content = train['content']
                tags_str = ""
                if len(tags) > 0:
                    for tag in tags:
                        tags_str = tags_str + tag + ","
                train['tags'] = tags_str

                trainItem.tags = tags_str
                geo = item['geo']
                if len(geo) > 0:
                    train['latitude'] = geo[0]
                    train['longitude'] = geo[1]
                train['longitude'] = ''
                train['latitude'] = ''
                if len(geo) == 2:
                    train['longitude'] = geo[0]
                    train['latitude'] = geo[1]
                imgs_str = ''
                trainItem.latitude = train['latitude']
                trainItem.longitude = train['longitude']
                try:
                    images = item['images']
                    if len(images) > 0:
                        for img in images:
                            imgs_str = img + "," + imgs_str

                    train['photo'] = item['photo']
                    trainItem.photo = item['photo']
                except Exception as e:
                    pass
                train['created'] = item['created']
                trainItem.created = item['created']
                train['images'] = imgs_str
                trainItem.images = imgs_str
                self.insert_train(trainItem)
                result.append(train)
        else:
            print(userId + "的列表已爬取完毕")
        return result

    def insert_train(self, train):
        try:
            self.db.ping(reconnect=True)

            data = (
                train.id, train.author_id, train.author_name, train.content.replace("'", "—"), train.tags,
                train.latitude,
                train.longitude,
                train.images, train.created, train.photo)
            result = self.cursor.execute(self.insert_train_sql % data)
            if result > 0:
                print("insert_train插入结果：", result)

            self.db.commit()
        except Exception as e:
            # print(e)
            pass

    def insert_user(self, keepuser):
        try:
            self.db.ping(reconnect=True)
            userid = keepuser.get('_id')
            self.cursor.execute(self.query_user_sql % userid)
            olduser = self.cursor.fetchone()
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
            result = self.cursor.execute(self.insert_user_sql % data)
            self.db.commit()
            if result == 1:
                print("插入一条新用户数据")

        except Exception as e:
            print(e)
        # getUserEntries(keepuser.get('_id'),"")

    def count_user_duration2(self):
        self.cursor.execute(self.count_user_duration_sql)
        result = self.cursor.fetchall()
        tag_one_months = '一个月'
        tag_three_months = '三个月'
        tag_half_year = '半年'
        tag_year = '一年'
        tag_one_and_half_year = '一年半'
        tag_two_years = '两年'
        tag_over_two_years = '两年以上'
        map = {tag_one_months: 0, tag_three_months: 0, tag_half_year: 0, tag_year: 0, tag_one_and_half_year: 0,
               tag_two_years: 0, tag_over_two_years: 0}
        du = []
        for item in result:
            duration = int(item['duration'])
            count = item['count']
            du.append(duration)
            if duration < 30 * 24 * 60:
                map[tag_one_months] = map[tag_one_months] + count
            elif duration <= 30 * 24 * 60 * 3:
                map[tag_three_months] = map[tag_three_months] + count
            elif duration <= 30 * 24 * 60 * 6:
                map[tag_half_year] = map[tag_half_year] + count
            elif duration <= 30 * 24 * 60 * 12:
                map[tag_year] = map[tag_year] + count
            elif duration <= 30 * 24 * 60 * 18:
                map[tag_one_and_half_year] = map[tag_one_and_half_year] + count
            elif duration <= 30 * 24 * 60 * 24:
                map[tag_two_years] = map[tag_two_years] + count
            elif duration > 24 * 30 * 24 * 60:
                map[tag_over_two_years] = map[tag_over_two_years] + count

        print('max = %s' % (numpy.max(du)))
        return map

    def count_user_duration(self):
        self.cursor.execute(self.count_user_duration_sql)
        result = self.cursor.fetchall()
        tag_one_hour = '一小时'
        tag_24_hours = '二十四小时'
        tag_three_days = '三天'
        tag_one_week = '一周'
        tag_one_month = '一个月'
        tag_three_months = '三个月'
        tag_one_years = '一年'
        tag_two_years = '两年'
        tag_over_two_years = '两年以上'
        map = {tag_one_hour: 0, tag_24_hours: 0, tag_three_days: 0, tag_one_week: 0, tag_one_month: 0,
               tag_three_months: 0, tag_one_years: 0, tag_two_years: 0, tag_over_two_years: 0}
        du = []
        for item in result:
            duration = int(item['duration'])
            count = item['count']
            du.append(duration)
            if duration < 60:
                map[tag_one_hour] = map[tag_one_hour] + count
            elif duration <= 24 * 60:
                map[tag_24_hours] = map[tag_24_hours] + count
            elif duration <= 3 * 24 * 60:
                map[tag_three_days] = map[tag_three_days] + count
            elif duration <= 7 * 24 * 60:
                map[tag_one_week] = map[tag_one_week] + count
            elif duration <= 30 * 24 * 60:
                map[tag_one_month] = map[tag_one_month] + count
            elif duration <= 30 * 24 * 60 * 3:
                map[tag_three_months] = map[tag_three_months] + count
            elif 12 * 30 * 24 * 60 < duration:
                map[tag_one_years] = map[tag_one_years] + count
            elif 24 * 30 * 24 * 60 <= duration:
                map[tag_two_years] = map[tag_two_years] + count
            elif duration > 24 * 30 * 24 * 60:
                map[tag_over_two_years] = map[tag_over_two_years] + count

        print('max = %s' % (numpy.max(du)))
        return map

    count_user_runningDistance_sql = 'select * from(select count(*) as count,runningDistance as dis from keep_user_info where runningDistance !="None" and runningDistance>0 group by runningDistance) t order by t.dis desc;'

    def count_user_dis(self):
        self.cursor.execute(self.count_user_runningDistance_sql)
        result = self.cursor.fetchall()
        tag_10_dis = '10km'
        tag_50_dis = '50km'
        tag_100_dis = '100km'
        tag_150_dis = '150km'
        tag_200_dis = '200km'
        tag_500_dis = '500km'
        tag_1000_dis = '1000km'
        tag_over_1000_dis = '超过1000km'
        mapData = {tag_10_dis: 0, tag_50_dis: 0, tag_100_dis: 0, tag_150_dis: 0, tag_200_dis: 0, tag_500_dis: 0,
                   tag_1000_dis: 0, tag_over_1000_dis: 0}
        for item in result:
            dis = float(item['dis'])
            count = item['count']
            if dis <= 10:
                mapData[tag_10_dis] = count + mapData[tag_10_dis]
            elif 10 < dis <= 50:
                mapData[tag_50_dis] = count + mapData[tag_50_dis]
            elif dis <= 100:
                mapData[tag_100_dis] = count + mapData[tag_100_dis]
            elif dis <= 150:
                mapData[tag_150_dis] = count + mapData[tag_150_dis]
            elif dis <= 200:
                mapData[tag_200_dis] = count + mapData[tag_200_dis]
            elif dis <= 500:
                mapData[tag_500_dis] = count + mapData[tag_500_dis]
            elif dis <= 1000:
                mapData[tag_1000_dis] = count + mapData[tag_1000_dis]
            elif dis > 1000:
                mapData[tag_over_1000_dis] = count + mapData[tag_over_1000_dis]
        return mapData

    def get_user_join_time(self):

        query_2015_user_count = self.query_user_timerange_sql % (1420041600, 1451577599)
        query_2016_user_count = self.query_user_timerange_sql % (1451577600, 1483199999)
        query_2017_user_count = self.query_user_timerange_sql % (1483200000, 1514735999)
        query_2018_user_count = self.query_user_timerange_sql % (1514736000, 1546271999)
        self.cursor.execute(query_2015_user_count)
        count_2015 = self.cursor.fetchone()['count']
        self.cursor.execute(query_2016_user_count)
        count_2016 = self.cursor.fetchone()['count']
        self.cursor.execute(query_2017_user_count)
        count_2017 = self.cursor.fetchone()['count']
        self.cursor.execute(query_2018_user_count)
        count_2018 = self.cursor.fetchone()['count']
        return {'2015': count_2015, "2016": count_2016, '2017': count_2017, '2018': count_2018}

    def get_user_month_of_year(self, year):
        min = '%s-01-01 00:00:00'
        max = '%s-12-31 23:59:59'
        divTime = 30 * 24 * 60 * 60 - 1
        timeTmp = int(time.mktime(time.strptime(min % year, "%Y-%m-%d %H:%M:%S")))
        # timeMax = int(time.mktime(time.strptime(max % year, "%Y-%m-%d %H:%M:%S")))
        months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        map = {}
        for month in months:
            index = month.index('月')
            value = int(month[0:index])
            timeStart = timeTmp + (value - 1) * divTime
            timeEnd = timeTmp + value * divTime
            self.cursor.execute(self.query_user_timerange_sql % (timeStart, timeEnd))
            count = self.cursor.fetchone()['count']
            map[month] = count

        return map

    def get_country_user_bmi_data(self):
        self.cursor.execute(self.country_user_bmi_sql)
        result = self.cursor.fetchall()
        return result

    # 获取所有城市的用户分布
    def get_all_city_user_data(self):
        self.cursor.execute(self.all_city_user_sql)
        result = self.cursor.fetchall()
        return result

    # 查询某个省的城市用户分布
    def get_province_city_user_data(self, province='广东省'):
        self.cursor.execute(self.province_city_user_sql % province)
        result = self.cursor.fetchall()
        return result

    province_data_sql = '''
     select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>0 and province != '银河' and province != '銀河' and country='中国'  group by province ) as t  group by t.province        '''

    # 获取全国各省的用户分布
    def get_country_user_data(self):
        self.cursor.execute(self.province_data_sql)
        result = self.cursor.fetchall()
        map = {}
        for item in result:
            province = item['province']
            count = item['count']
            if province == '台湾' or province == '台灣' or province == '台灣省':
                if map.__contains__('台湾省'):
                    map['台湾省'] = map['台湾省'] + count
                else:
                    map['台湾省'] = count
                province = '台湾省'
            elif province == '廣東省':
                if map.__contains__('广东省'):
                    map['广东省'] = map['广东省'] + count
                    pass
                else:
                    map['广东省'] = count

                province = '广东省'
            elif province == '廣西壯族自治區':
                if map.__contains__('广西壮族自治区'):
                    map['广西壮族自治区'] = map['广西壮族自治区'] + count
                    pass
                else:
                    map['广西壮族自治区'] = count

                province = '广西壮族自治区'
            elif province == '新疆維吾爾自治區':
                if map.__contains__('新疆维吾尔自治区'):
                    map['新疆维吾尔自治区'] = map['新疆维吾尔自治区'] + count
                    pass
                else:
                    map['新疆维吾尔自治区'] = count

                province = '新疆维吾尔自治区'
            elif province == '重慶市':
                if map.__contains__('重庆市'):
                    map['重庆市'] = map['重庆市'] + count
                    pass
                else:
                    map['重庆市'] = count

                province = '重庆市'
            elif province == '雲南省':
                if map.__contains__('云南省'):
                    map['云南省'] = map['云南省'] + count
                    pass
                else:
                    map['云南省'] = count

                province = '云南省'
            elif province == '山東省':
                if map.__contains__('山西省'):
                    map['山西省'] = map['山西省'] + count
                    pass
                else:
                    map['山西省'] = count

                province = '云南省'
            elif province == '香港特別行政區':
                if map.__contains__('香港特别行政区'):
                    map['香港特别行政区'] = map['香港特别行政区'] + count
                    pass
                else:
                    map['香港特别行政区'] = count

                province = '香港特别行政区'
            elif province == '澳門特別行政區':
                if map.__contains__('澳门特别行政区'):
                    map['澳门特别行政区'] = map['澳门特别行政区'] + count
                    pass
                else:
                    map['澳门特别行政区'] = count

                province = '澳门特别行政区'
            else:
                map[province] = count
        return map

    query_province_list_sql = '''
            select distinct province from keep_user_info where length(province)>0 and province != 'None' and country="中国"
        '''

    # 获取省份列表
    def get_province_list(self):
        self.cursor.execute(self.query_province_list_sql)
        result = self.cursor.fetchall()
        return result

    query_shaoshuminzu_sql = '''
            select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>12 and province not like '香%' and province not like '澳%' and country='中国'  group by province ) as t  group by t.province
            '''

    def get_shaoshu_minzu_data(self):
        self.cursor.execute(self.query_shaoshuminzu_sql)
        result = self.cursor.fetchall()
        return result

    # 获取直辖市列表

    query_zhixia_city_list_sql = '''
        select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>0 and country='中国' and province like '%市' group by province ) as t  group by t.province
    '''

    # 获取直辖市列表
    def get_zhixia_city_list(self):
        self.cursor.execute(self.query_zhixia_city_list_sql)
        result = self.cursor.fetchall()
        return result

    # 获取某个城市的用户年龄分布情况
    def get_city_user_age_data(self, city='深圳市'):
        self.cursor.execute(self.birthday_of_city_sql % city)
        result = self.cursor.fetchall()
        tag_60s = '50，60后'
        tag_70s = '70后'
        tag_80s = '80后'
        tag_85s = '85后'
        tag_90s = '90后'
        tag_95s = '95后'
        tag_00s = '00后'
        mapData = {tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
        for item in result:
            bd = item['bd']
            count = item['count']
            if 1950 <= bd < 1970:
                mapData[tag_60s] = mapData[tag_60s] + count
            elif 1970 <= bd < 1980:
                mapData[tag_70s] = mapData[tag_70s] + count
            elif 1980 <= bd < 1985:
                mapData[tag_80s] = mapData[tag_80s] + count
            elif 1985 <= bd < 1990:
                mapData[tag_85s] = mapData[tag_85s] + count
            elif 1990 <= bd < 1995:
                mapData[tag_90s] = mapData[tag_90s] + count
            elif 1995 <= bd < 2000:
                mapData[tag_95s] = mapData[tag_95s] + count
            elif 2000 <= bd < 2010:
                mapData[tag_00s] = mapData[tag_00s] + count

        return mapData

    # 查询某个省的用户年龄分布
    def get_province_user_age_data(self, province="广东省"):
        self.cursor.execute(self.birthday_of_province_sql % province)
        result = self.cursor.fetchall()
        tag_60s = '50，60后'
        tag_70s = '70后'
        tag_80s = '80后'
        tag_85s = '85后'
        tag_90s = '90后'
        tag_95s = '95后'
        tag_00s = '00后'
        mapData = {tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
        total = 0
        for item in result:
            bd = item['bd']
            count = item['count']
            total = total + count
            if 1950 <= bd < 1970:
                mapData[tag_60s] = mapData[tag_60s] + count
            elif 1970 <= bd < 1980:
                mapData[tag_70s] = mapData[tag_70s] + count
            elif 1980 <= bd < 1985:
                mapData[tag_80s] = mapData[tag_80s] + count
            elif 1985 <= bd < 1990:
                mapData[tag_85s] = mapData[tag_85s] + count
            elif 1990 <= bd < 1995:
                mapData[tag_90s] = mapData[tag_90s] + count
            elif 1995 <= bd < 2000:
                mapData[tag_95s] = mapData[tag_95s] + count
            elif 2000 <= bd < 2010:
                mapData[tag_00s] = mapData[tag_00s] + count

        return mapData

    # 获取全国用户的年龄分布
    def get_country_user_age_data(self):
        self.cursor.execute(self.birthday_sql)
        result = self.cursor.fetchall()
        tag_60s = '50，60后'
        tag_70s = '70后'
        tag_80s = '80后'
        tag_85s = '85后'
        tag_90s = '90后'
        tag_95s = '95后'
        tag_00s = '00后'
        mapData = {tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
        for item in result:
            bd = item['bd']
            count = item['count']
            if 1950 <= bd < 1970:
                mapData[tag_60s] = mapData[tag_60s] + count
            elif 1970 <= bd < 1980:
                mapData[tag_70s] = mapData[tag_70s] + count
            elif 1980 <= bd < 1985:
                mapData[tag_80s] = mapData[tag_80s] + count
            elif 1985 <= bd < 1990:
                mapData[tag_85s] = mapData[tag_85s] + count
            elif 1990 <= bd < 1995:
                mapData[tag_90s] = mapData[tag_90s] + count
            elif 1995 <= bd < 2000:
                mapData[tag_95s] = mapData[tag_95s] + count
            elif 2000 <= bd < 2010:
                mapData[tag_00s] = mapData[tag_00s] + count
        return mapData
