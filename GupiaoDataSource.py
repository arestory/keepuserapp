import pymysql
import time
import datetime
from urllib import request
from pandas.tseries.offsets import Day


class GupiaoDs(object):
    index_url = 'http://hq.sinajs.cn/list=%s%s'

    db = pymysql.connect("212.64.93.216", 'root', 'yuwenque', 'mago', charset='utf8mb4', autocommit=True)

    cursor = db.cursor(pymysql.cursors.DictCursor)

    def create_tables(self):
        sql1 = 'create table stock_yes(id varchar(10) primary  key ,name varchar(20) not null ,vol_on_up INTEGER not null ,create_time varchar(30) not  null )'
        sql2 = 'create table stock_925(id varchar(10) primary  key ,name varchar(20) not null ,call_auction INTEGER not null ,create_time varchar(30) not  null )'
        self.cursor.execute(sql1)
        self.cursor.execute(sql2)
        self.db.commit()

    def get_gp_info(self, id):
        sql = 'select * from stock_yes where id ="%s"' % id
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            return result
        return []

    # 查询数据库是否存在9.25的记录
    def get_gp_info_on925_table(self, id):
        time_stamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        time_stamp = time_stamp + ",09:25"
        sql = 'select * from stock_925 where id ="%s" and create_time = "%s"' % (id, time_stamp)
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_gp_info_on_time(self, id):
        try:
            start = id[0:1]
            if start == '3' or start == '0' or start == '1' or start == '2':
                url = self.index_url % ('sz', id)

            elif start == '6':
                url = self.index_url % ('sh', id)
            print(url)
            # r = requests.get(url,headers=header,verify=False)
            r = request.urlopen(url)
            # r = requests.request("GET",url)
            content = str(r.read().decode('gbk'))
            arr = str(content).split(',')
            if len(arr) > 1:
                arr[0] = arr[0].split("\"")[1]

                call_auction = arr[8]
                index = len(arr) - 1
                date = arr[index - 2]
                time_minute = arr[index - 1][0:5]
                timestamp = date + "," + time_minute
                print("当前数据时刻 ： %s" % timestamp)
                map = {'id': id, 'name': arr[0], 'call_auction': int(call_auction), 'create_time': timestamp}
                # 保存9。25的数据
                if time_minute == '09:25':
                    self.add_stock925(id, arr[0], call_auction, timestamp)
                    return map
                return map
            else:
                map = {'id': id, 'name': '未知/不存在该股票：'+id, 'call_auction': int(1), 'create_time': '1970-01-01'}
                return map

        except Exception as e:
            return {}


    def add_stock925(self, code, name, call_auction, time_stamp):
        try:
            sql = '''
                      insert into stock_925(id,name,call_auction,create_time) values ('%s','%s',%s,'%s')
                  ''' % (code, name, int(call_auction), time_stamp)
            print(sql)
            result = self.cursor.execute(sql)
            print('result = %s' % result)
            self.db.commit()
        except Exception as e:
            result = -1
        return result

    def add_stock(self, code, name, vol_on_up,create_time):
        try:
            if not create_time:
                time_stamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            else:
                time_stamp=create_time
            sql = '''
                replace into stock_yes(id,name,vol_on_up,create_time) values ('%s','%s',%s,'%s')
            ''' % (code, name, int(vol_on_up), time_stamp)
            print(sql)
            result = self.cursor.execute(sql)
            print('result = %s' % result)
            self.db.commit()
        except Exception as e:
            result = -1
        return result

    def delete_today_add_stock(self, code):
        sql = '''
            delete from stock_yes where id = '%s'
        ''' % code
        result = self.cursor.execute(sql)
        self.db.commit()
        return result

    def query_add_stocks_with_date(self,date):
        sql = ''' select * from stock_yes where create_time ='%s'
                     ''' % date
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        return result_list

    def query_today_add_stocks(self,date):
        if not date:
            now_time = datetime.datetime.now()  # 获取当前时间
            date = now_time.strftime('%Y-%m-%d')  # 格式化

        # 获取昨天的数据
        sql = '''
                   select * from stock_yes where create_time ="%s"
               ''' % date
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        return result_list

    def query_yesterday_stock(self):
        now_time = datetime.datetime.now()  # 获取当前时间
        yes_time = (now_time - 1 * Day()).strftime('%Y-%m-%d')  # 格式化
        # 获取昨天的数据
        sql = '''
            select * from stock_yes where create_time ="%s"
        ''' % yes_time
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        return result_list

    def get_stock_list_detail(self, stock_list):
        for code in stock_list:
            map = self.get_gp_info_on_time(code)
            self.add_stock(code, map['name'], map['call_auction'])
            pass

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        self.db.commit()


ds = GupiaoDs()
# ds.get_stock_list_detail(['300263', '600267', '300262', '600266', '300261', '600265'])
ds.execute_sql('''

replace into stock_925(id,name,call_auction,create_time) values ('600265','ST景谷',171388,'2019-02-17,09:25')
''')
ds.execute_sql('''
                replace into stock_925(id,name,call_auction,create_time) values ('300261','雅本化学',2418823,'2019-02-17,09:25')
''')
ds.execute_sql('''
                replace into stock_925(id,name,call_auction,create_time) values ('600266','北京城建',5894236,'2019-02-17,09:25')

''')
ds.execute_sql('''
                replace into stock_925(id,name,call_auction,create_time) values ('300262','巴安水务',12172399,'2019-02-17,09:25')

''')
ds.execute_sql('''
                replace into stock_925(id,name,call_auction,create_time) values ('600267','海正药业',11701781,'2019-02-17,09:25')
 

''')
ds.execute_sql('''
                replace into stock_925(id,name,call_auction,create_time) values ('300263','隆华科技',116328079,'2019-02-17,09:25')

''')
# ds.create_tables()

# ds.add_stock('300263', '隆华科技', '85814043')
# contents = ds.get_gp_info_on_time('300263')

# print(contents)
import sys

# get_stock_list_detail(['300263', '600267'])
