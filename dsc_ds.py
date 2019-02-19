# coding=UTF-8
import pymysql.cursors
import time, datetime
import numpy
import requests
import threading
import json


class DscDatasource(object):
    # db = pymysql.connect("212.64.93.216", 'root', 'yuwenque', 'dsc', charset='utf8mb4', port=3306,
    #                      cursorclass=pymysql.cursors.DictCursor)
    db = pymysql.connect("localhost", 'root', 'yuwenque', 'dsc', charset='utf8mb4', port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    insert_user_sql = '''insert ignore INTO userinfo (id,name,os_type,birthday,update_time,city,sex,birthpet,avatar,education,university,
    star_sign,ideal_mate,hometown,height,weight,characters ,station,company,hobby,referee_id,referee_name)   VALUES (
    "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") '''


    sql1='''
     select count(*) as num ,left(name,1) as first from userinfo group by left(name,1) order by num desc
    '''
    sql2='''
    select count(*) as num ,right(name,1) as lastname from userinfo where birthday like '199%' group by lastname order by num desc;

    '''
    sql3 = '''
    select count(*) as num,university from userinfo where birthday like '199%' group by university  order by num desc
    '''

    sql4 = '''
    select count(*) as num ,left(birthday,4) as birth from userinfo where education ='硕士' group by birth order by num desc;
    
    '''

    sql5='''
    select count(*) as num,education from userinfo group by education order by num desc;
    '''
    birthpetMap = {

        '鼠': '1',
        '牛': '2',
        '虎': '3',
        '兔': '4',
        '龙': '5',
        '蛇': '6',
        '马': '7',
        '羊': '8',
        '猴': '9',
        '鸡': '10',
        '狗': '11',
        '猪': '12',
    }

    def pingDb(self):
        self.db.ping(reconnect=True)

    def execute_sql(self,sql):
        self.cursor.execute(sql)
        self.db.commit()

    def update_user_time(self,userId,update_time):
        try:
            self.db.ping(reconnect=True)
            sql = '''update userinfo set update_time = "%s" where id = "%s" ''' % (update_time,userId)
            result = self.cursor.execute(sql)
            self.db.commit()
            if result == 1:
                 print(userId+"更新成功")

        except Exception as e:
            print("更新失败，id="+userId)
            pass

    def insert(self, user):

        print(user)
        print('-----')
        try:

            self.db.ping(reconnect=True)

            sql = self.insert_user_sql % (
                user['id'], user['name'], user['os_type'], user['birthday'], user['update_time'][0:10], user['city'],
                user['sex'], user['birthpet'],
                user['avatar'], user['education'], user['university'], user['star_sign'], user['ideal_mate'],
                user['hometown'],
                user['height'],
                user['weight'], user['characters'], user['station'], user['company'], user['hobby'], user['referee_id'],
                user['referee_name'])

            print(sql)
            result = self.cursor.execute(sql)
            print("sql 结果 :%s" % result)
            if result > 0:
                print(
                    "%s , %s,%s %s(cm),%s(kg)" % (
                        user['name'], user['birthday'], user['city'], user['height'], user['weight']))
                self.db.commit()

        except Exception as e:
            print(e)
            pass

    def execute_sql(self,sql):
        print(sql)
        result = self.cursor.execute(sql)
        self.db.commit()
        print("sql 结果 %s" % result)


    # 获取用户详情
    def get_user_info(self, userId):
        query_user_info = '''select * from userinfo where id = "%s" ''' % userId
        self.cursor.execute(query_user_info)
        return self.cursor.fetchone()

    # 获取用户列表
    def get_user_list(self, start, count):
        self.pingDb()
        query_user_list = ''' 
        select * from userinfo limit %s,%s
        ''' % (start, count)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        return query_result


    # 获取用户列表
    def get_user_id_list_without_update_time(self, start, count):
        try:
            self.pingDb()
            query_user_list = ''' 
                    select id from userinfo  where update_time =0 and left(birthday,4)>=1990 limit %s,%s
                    ''' % (start, count)
            self.cursor.execute(query_user_list)
            query_result = self.cursor.fetchall()
            return query_result
        except Exception as e:
            print(e)



    # 获取某个公司的用户列表
    def get_user_list_from_company(self, keyword, start, count):
        self.pingDb()
        query_user_list = ''' 
               select * from userinfo where company like '%%%s%%' limit %s,%s
               ''' % (keyword, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个生日年份的用户列表
    def get_user_list_between_birthday(self, year, start, count):
        self.pingDb()
        query_user_list = ''' 
                     select * from userinfo where left(birthday,4)>= %s limit %s,%s
                     ''' % (year, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        print(len(query_result))
        return query_result

    # 获取某个生肖的用户列表
    def get_user_list_with_birthpet(self, pet, start, count):
        self.pingDb()
        query_user_list = ''' 
                     select * from userinfo where birthpet ="%s" limit %s,%s
                     ''' % (pet, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个身高范围的用户列表
    def get_user_list_between_height(self, heightMin, heightMax, start, count):
        self.pingDb()
        query_user_list = ''' 
                     select * from userinfo where height>=%s and height<=%s limit %s,%s
                     ''' % (heightMin, heightMax, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个体重范围的用户列表
    def get_user_list_between_weight(self, weightMin, weightMax, start, count):
        self.pingDb()
        query_user_list = ''' 
                     select * from userinfo where weight>=%s and weight<=%s limit %s,%s
                     ''' % (weightMin, weightMax, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取大于某个身高的用户列表
    def get_user_list_target_height(self, heightMin, start, count):
        self.pingDb()
        query_user_list = ''' 
                     select * from userinfo where height>=%s limit %s,%s
                     ''' % (heightMin, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个星座的用户列表
    def get_user_list_star_sign(self, star_sign, start, count):
        self.pingDb()
        query_user_list = ''' 
                            select * from userinfo where star_sign="%s" limit %s,%s
                            ''' % (star_sign, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个学历的用户列表
    def get_user_list_with_education(self, education, start, count):
        self.pingDb()
        query_user_list = ''' 
                            select * from userinfo where education="%s" limit %s,%s
                            ''' % (education, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个学校的用户列表
    def get_user_list_with_university(self, university, start, count):
        self.pingDb()
        query_user_list = ''' 
                            select * from userinfo where university="%s" limit %s,%s
                            ''' % (university, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取某个地区的用户列表
    def get_user_list_with_area(self, area, start, count):
        self.pingDb()
        query_user_list = ''' 
                            select * from userinfo where hometown like '%%%s%%' limit %s,%s
                            ''' % (area, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 多重查询
    def get_user_with_complicate(self,area,birth,height,name,university,start,count):
        self.pingDb()
        query_user_list = ''' 
                                  select * from userinfo where name like '%%%s%%' and university like '%%%s%%' and hometown like '%%%s%%' and left(birthday,4)>=%s and height>%s
 limit %s,%s                                  ''' % (name,university,area, birth, height,start,count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个地区的年龄段的用户列表
    def get_user_list_with_area_and_birth(self, area, birth,height, start, count):
        self.pingDb()
        query_user_list = ''' 
                            select * from userinfo where hometown like '%%%s%%' and left(birthday,4)>=%s and height>%s limit %s,%s
                            ''' % (area, birth, height,start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个兴趣关键字的用户列表
    def get_user_list_with_hobby(self, hobby, start, count):
        self.pingDb()
        query_user_list = ''' 
                            select * from userinfo where hobby like '%%%s%%' limit %s,%s
                            ''' % (hobby, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    def get_user_with_name(self,name, start, count):
        query_user_list = ''' 
                                  select * from userinfo where id = "%s" limit %s,%s
                                  ''' % (name, start, count)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result
    def get_user_list_with_company_and_birth(self, company, birthday):
        self.pingDb()

        query_user_list = ''' 
                            select * from userinfo where company like '%%%s%%' and birthday like '%s%%'
                            ''' % (company, birthday)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

#
# ds = DscDatasource()

# ds.execute_sql('''
# insert ignore INTO userinfo (id,name,os_type,birthday,update_time,city,sex,birthpet,avatar,education,university,
#     star_sign,ideal_mate,hometown,height,weight,characters ,station,company,hobby,referee_id,referee_name)   VALUES (
#     '104211','况招霞','ios','1987-10-29','2019-02-15 22:02:09','深圳','female','4','https://release.image.dscapp.dscun.com/avatar/B4F7C8B1-4310-4907-BC53-B67A6CE5544F.jpg','硕士','STU','天蝎座','善良纯粹乐观平和','江西 宜春','158','41','对未来充满了好奇，最好奇的事情还是你会是谁。','医生','深圳某医院','读书骑行徒步爬山花草茶诗','1','杨村长')
#
#
# ''')
#
# query_result = ds.get_user_list_with_area_and_birth('湛江','199',1,1000)
# print(len(query_result))

# ds.get_user_with_name('117302',1,100)
# print(ds.get_user_with_complicate('','1996',0,'丽芳',""))