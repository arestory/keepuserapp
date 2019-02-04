# coding=UTF-8
import pymysql.cursors

import time, datetime
import numpy
import requests
import threading
import json


class DscDatasource(object):
    db = pymysql.connect("212.64.93.216", 'root', 'yuwenque', 'dsc', charset='utf8mb4', port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

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

    # 获取用户列表
    def get_user_list(self, start, end):
        query_user_list = ''' 
        select * from user limit %s,%s
        ''' % (start, end)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        return query_result

    # 获取某个公司的用户列表
    def get_user_list_from_company(self, keyword, start, end):
        query_user_list = ''' 
               select * from user where company like '%%%s%%' limit %s,%s
               ''' % (keyword, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个生日年份的用户列表
    def get_user_list_between_birthday(self, year, start, end):
        query_user_list = ''' 
                     select * from user where birthday like '%s%%' limit %s,%s
                     ''' % (year, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个生肖的用户列表
    def get_user_list_with_birthpet(self, pet, start, end):
        query_user_list = ''' 
                     select * from user where birthpet ='%s' limit %s,%s
                     ''' % (pet, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个身高范围的用户列表
    def get_user_list_between_height(self, heightMin, heightMax, start, end):
        query_user_list = ''' 
                     select * from user where height>=%s and height<=%s limit %s,%s
                     ''' % (heightMin, heightMax, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取某个体重范围的用户列表
    def get_user_list_between_weight(self, weightMin, weightMax, start, end):
        query_user_list = ''' 
                     select * from user where weight>=%s and weight<=%s limit %s,%s
                     ''' % (weightMin, weightMax, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取大于某个身高的用户列表
    def get_user_list_target_height(self, heightMin, start, end):
        query_user_list = ''' 
                     select * from user where height>=%s limit %s,%s
                     ''' % (heightMin, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取某个星座的用户列表
    def get_user_list_star_sign(self, star_sign, start, end):
        query_user_list = ''' 
                            select * from user where star_sign='%s' limit %s,%s
                            ''' % (star_sign, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取某个学历的用户列表
    def get_user_list_with_education(self, education, start, end):
        query_user_list = ''' 
                            select * from user where education='%s' limit %s,%s
                            ''' % (education, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取某个学校的用户列表
    def get_user_list_with_university(self, university, start, end):
        query_user_list = ''' 
                            select * from user where university='%s' limit %s,%s
                            ''' % (university, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result


    # 获取某个地区的用户列表
    def get_user_list_with_area(self, area, start, end):
        query_user_list = ''' 
                            select * from user where hometown like '%%%s%%' limit %s,%s
                            ''' % (area, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个地区的年龄段的用户列表
    def get_user_list_with_area_and_birth(self, area, birth,start, end):
        query_user_list = ''' 
                            select * from user where hometown like '%%%s%%' and birthday like '%s%%' limit %s,%s
                            ''' % (area,birth, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    # 获取某个兴趣关键字的用户列表
    def get_user_list_with_hobby(self, hobby, start, end):
        query_user_list = ''' 
                            select * from user where hobby like '%%%s%%' limit %s,%s
                            ''' % (hobby, start, end)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result

    def get_user_list_with_company_and_birth(self,company,birthday):

        query_user_list = ''' 
                            select * from user where company like '%%%s%%' and birthday like '%s%%'
                            ''' % (company,birthday)
        print(query_user_list)
        self.cursor.execute(query_user_list)
        query_result = self.cursor.fetchall()
        print(query_result)
        return query_result



ds = DscDatasource()

query_result = ds.get_user_list_with_area_and_birth('广东','19',1,1000)
print(len(query_result))