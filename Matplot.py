import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy
import matplotlib
import pymysql.cursors
import json
import time

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
            where city='%s' and birthday NOT LIKE '1900%%' and birthday != 'None' and birthday not like '201%%' ) 
          as t group by t.bd
'''

# 必须指定cursorclass，否则查询的返回结果不包含字段
db = pymysql.connect("localhost", 'root', 'yuwenque', 'keep', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()


# 查询某个省的城市用户分布
def show_province_city_user(province='广东省'):
    sql = '''
    select t.count,t.city from ( select count(*) as count ,city from keep_user_info where province='%s' group by city) as t
    '''
    cursor.execute(sql % province)
    result = cursor.fetchall()
    labels = []
    data = []
    for item in result:
        city = item['city']
        count = item['count']
        print(item)
        labels.append(city)
        data.append(count)

    pie = plt.pie(data, labels=labels, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12}, pctdistance=0.85)
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(
            matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

    # 解决标题中文乱码
    plt.title("%s城市用户分布" % province, fontproperties=font, loc='right')
    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()

    pass


show_province_city_user('广西壮族自治区')


# 展示全国用户的年龄分布
def show_country_pie():
    sql = '''
 select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>0 and province != '银河' and province != '銀河' and country='中国'  group by province ) as t  group by t.province        '''
    cursor.execute(sql)
    result = cursor.fetchall()
    labels = []
    data = []
    max = result[0]['count']
    min = result[len(result) - 1]['count']
    print('max = %s ,min = %s' % (max, min))
    map = {}
    zizhiqu = {'count': 0}
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

        if len(province) > 4:
            zizhiqu['count'] = zizhiqu['count'] + count
        else:
            pass
    totalCount = 0
    for k in map.keys():
        if map[k] > 0:
            labels.append(k)
            data.append(map[k])
            print('%s人数：%s' % (k, map[k]))
            totalCount = totalCount + map[k]
        pass

    print("全国用户数：%s" % totalCount)
    # labels.append('各自治区')
    # data.append(zizhiqu['count'])
    pie = plt.pie(data, labels=labels, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12}, pctdistance=0.85)
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(
            matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

    # 解决标题中文乱码
    plt.title("全国用户分布", fontproperties=font, loc='right')
    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()


# show_country_pie()


def show_province_bar():
    sql = '''
 select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>0 and country='中国'  group by province ) as t  group by t.province  order by t.count  desc     '''
    cursor.execute(sql)
    result = cursor.fetchall()
    labels = []
    data = []
    for item in result:
        citycode = item['province']
        count = item['count']
        labels.append(citycode)
        data.append(count)
    bar = plt.bar(labels, data)
    # 解决乱码问题
    # for font in bar:
    #     font.set_fontproperties(matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.show()


# show_province_bar()


def show_all_province():
    sql = '''
        select distinct province from keep_user_info where length(province)>0 and province != 'None' and country="中国"
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    for item in result:
        time.sleep(1)
        show_province_user_age_pie(item['province'])
    pass


# show_all_province()

# 少数民族
def show_shaoshu():
    sql = '''
        select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>12 and province not like '香%' and province not like '澳%' and country='中国'  group by province ) as t  group by t.province
        '''
    cursor.execute(sql)
    result = cursor.fetchall()
    labels = []
    data = []
    total = 0
    for item in result:
        province = item['province']
        count = item['count']
        total = total + count
        if count>=5:
            labels.append(province)
            data.append(count)
    pie = plt.pie(data, labels=labels, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12}, pctdistance=0.7)

    print("自治区及特别行政区人数：%s" % total)
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

    # 解决标题中文乱码
    plt.title("自治区用户比例", fontproperties=font, loc='right')
    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()
    pass


# 直辖市用户比例
def show_zhixiashi():
    sql = '''
    select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>0 and country='中国' and province like '%市' group by province ) as t  group by t.province
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    labels = []
    data = []
    total = 0
    for item in result:
        province = item['province']
        count = item['count']
        total =total+count
        if province != '重慶市':
            labels.append(province)
            data.append(count)
    pie = plt.pie(data, labels=labels, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12}, pctdistance=0.7)

    print("直辖市人数：%s" % total)
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

    # 解决标题中文乱码
    plt.title("直辖市用户比例", fontproperties=font, loc='right')
    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()


# 查询某个市的用户年龄分布
def show_city_user_age_pie(city="深圳市"):
    cursor.execute(birthday_of_city_sql % city)
    result = cursor.fetchall()
    tag_60s = '50，60后'
    tag_70s = '70后'
    tag_80s = '80后'
    tag_85s = '85后'
    tag_90s = '90后'
    tag_95s = '95后'
    tag_00s = '00后'
    labels = tag_60s, tag_70s, tag_80s, tag_85s, tag_90s, tag_95s, tag_00s
    map = {tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
    total = 0
    for item in result:
        bd = item['bd']
        count = item['count']
        total = total + count
        if 1950 <= bd < 1970:
            map[tag_60s] = map[tag_60s] + count
            pass
        elif 1970 <= bd < 1980:
            map[tag_70s] = map[tag_70s] + count
            pass
        elif 1980 <= bd < 1985:
            map[tag_80s] = map[tag_80s] + count
        elif 1985 <= bd < 1990:
            map[tag_85s] = map[tag_85s] + count
            pass
        elif 1990 <= bd < 1995:
            map[tag_90s] = map[tag_90s] + count
            pass
        elif 1995 <= bd < 2000:
            map[tag_95s] = map[tag_95s] + count
            pass
        elif 2000 <= bd < 2010:
            map[tag_00s] = map[tag_00s] + count
            pass
        pass

    print("%s人数：%s" % (city, total))
    sizes = [map[tag_60s], map[tag_70s], map[tag_80s], map[tag_85s], map[tag_90s], map[tag_95s],
             map[tag_00s]]
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange', 'yellow', 'red', 'pink'
    explode = 0, 0, 0, 0, 0.1, 0, 0

    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)
    pie = plt.pie(sizes, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12})
    # 解决标题中文乱码
    plt.title("%s用户年龄分布" % city, fontproperties=font, loc='right')
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')

    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()


# show_city_user_age_pie()


# 查询某个省的用户年龄分布
def show_province_user_age_pie(province="广东省"):
    cursor.execute(birthday_of_province_sql % province)
    result = cursor.fetchall()
    tag_60s = '50，60后'
    tag_70s = '70后'
    tag_80s = '80后'
    tag_85s = '85后'
    tag_90s = '90后'
    tag_95s = '95后'
    tag_00s = '00后'
    labels = tag_60s, tag_70s, tag_80s, tag_85s, tag_90s, tag_95s, tag_00s
    map = {tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
    total = 0
    for item in result:
        bd = item['bd']
        count = item['count']
        total = total + count
        if 1950 <= bd < 1970:
            map[tag_60s] = map[tag_60s] + count
            pass
        elif 1970 <= bd < 1980:
            map[tag_70s] = map[tag_70s] + count
            pass
        elif 1980 <= bd < 1985:
            map[tag_80s] = map[tag_80s] + count
        elif 1985 <= bd < 1990:
            map[tag_85s] = map[tag_85s] + count
            pass
        elif 1990 <= bd < 1995:
            map[tag_90s] = map[tag_90s] + count
            pass
        elif 1995 <= bd < 2000:
            map[tag_95s] = map[tag_95s] + count
            pass
        elif 2000 <= bd < 2010:
            map[tag_00s] = map[tag_00s] + count
            pass
        pass

    print("%s人数：%s" % (province, total))
    sizes = [map[tag_60s], map[tag_70s], map[tag_80s], map[tag_85s], map[tag_90s], map[tag_95s],
             map[tag_00s]]
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange', 'yellow', 'red', 'pink'
    explode = 0, 0, 0, 0, 0.1, 0, 0

    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)
    pie = plt.pie(sizes, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12})
    # 解决标题中文乱码
    plt.title("%s用户年龄分布" % province, fontproperties=font, loc='right')
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')

    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()


# show_province_user_age_pie('山东省')


# show_zhixiashi()
def show_user_age_pie():
    cursor.execute(birthday_sql)
    result = cursor.fetchall()
    tag_60s = '50，60后'
    tag_70s = '70后'
    tag_80s = '80后'
    tag_85s = '85后'
    tag_90s = '90后'
    tag_95s = '95后'
    tag_00s = '00后'
    labels = tag_60s, tag_70s, tag_80s, tag_85s, tag_90s, tag_95s, tag_00s
    map = {tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
    for item in result:
        bd = item['bd']
        count = item['count']
        if 1950 <= bd < 1970:
            map[tag_60s] = map[tag_60s] + count
            pass
        elif 1970 <= bd < 1980:
            map[tag_70s] = map[tag_70s] + count
            pass
        elif 1980 <= bd < 1985:
            map[tag_80s] = map[tag_80s] + count
        elif 1985 <= bd < 1990:
            map[tag_85s] = map[tag_85s] + count
            pass
        elif 1990 <= bd < 1995:
            map[tag_90s] = map[tag_90s] + count
            pass
        elif 1995 <= bd < 2000:
            map[tag_95s] = map[tag_95s] + count
            pass
        elif 2000 <= bd < 2010:
            map[tag_00s] = map[tag_00s] + count
            pass
        pass
    sizes = [map[tag_60s], map[tag_70s], map[tag_80s], map[tag_85s], map[tag_90s], map[tag_95s],
             map[tag_00s]]
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange', 'yellow', 'red', 'pink'
    explode = 0, 0, 0, 0, 0, 0.1, 0, 0

    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)
    pie = plt.pie(sizes, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=40,
                  textprops={'fontsize': 12})
    # 解决标题中文乱码
    plt.title("keep用户年龄分布", fontproperties=font)
    # 解决乱码问题
    for font in pie[1]:
        font.set_fontproperties(matplotlib.font_manager.FontProperties(fname='/Library/Fonts/Songti.ttc'))

    plt.axis('equal')

    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #
    # plt.rcParams['font.family']=['Arial Black']

    plt.show()


# show_user_age_pie()


def show_user_city():
    sql = '''
     select t.province, t.count from (select count(*) as count,province from keep_user_info where length(province)>0 and city!="地球" group by province ) as t group by t.province order by t.count desc limit 25
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    max = result[0]['count']
    min = result[len(result) - 1]['count']
    print('max = %s,min = %s ' % (max, min))

    data = []
    province = []
    for item in result:
        # print(item)
        data.append(item['count'])
        province.append(item['province'])
        pass

    plt.bar(province, data)

    plt.show()

# show_user_city()
