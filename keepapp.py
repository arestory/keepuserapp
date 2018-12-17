from flask import Flask
from flask import request
from flask import Blueprint, render_template, send_file, send_from_directory
import numpy
import pymysql.cursors
import json
from flask import make_response

from pyecharts import Map, Pie, Bar,Line,Geo
from datasource import UserDatasource

app = Flask(__name__, static_url_path='')
# 必须指定cursorclass，否则查询的返回结果不包含字段
db = pymysql.connect("localhost", 'root', 'yuwenque', 'keep', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

query_user_info_sql = 'select * from keep_user where userid = "%s"'
query_user_num_sql = 'select count(*) from keep_user'
query_user_list_sql = 'select * from keep_user limit %s,%s'
query_user_train_list_sql = 'select * from keep_train where author_id = "%s"'
query_wx_user_list_sql = 'select * from keep_user where bio like "%%微信%%" and gender ="F" limit %s,%s'
query_top_train_list_sql = 'select * from keep_train limit %s,%s'
query_geo_train_list_sql = 'select * from keep_train where length(latitude)>0 limit %s,%s'

query_age_range_sql = '''
 select count(*) as count from
        (select cast(left(birthday,4) as SIGNED INTEGER) as bd FROM keep_user where birthday NOT LIKE '1900%%' and birthday != 'None')  
        t where t.bd >= %s and t.bd< %s
'''
query_city_users_sql = '''
select count(*) as count from keep_user where citycode = '%s'
'''

query_province_users_sql = '''
select count(*) as count from keep_user_info where province like '%s'
'''

query_city = '''  
select DISTINCT citycode,city from keep_user_info where length(city)>0 and length(citycode)>0 and country="中国"
  '''

query_province = '''  
select DISTINCT province from keep_user_info where length(province)>0 and country="中国"
  '''
query_city_users_count_sql = '''
select citycode,city ,count(*) as count from keep_user_info where length(city)>0 and length(citycode)>0 and country="中国" and city != '地球' group by city,citycode order by length(city)
'''
query_province_users_count_sql = '''
select province ,count(*) as count from keep_user_info where length(province)>0   and country="中国" group by province order by length(province)
'''


# The view function did not return a valid response.
# The return type must be a string, tuple,
#  Response instance, or WSGI callable, but it was a dict.
@app.route('/user_age_range/', methods=['GET'])
def get_age_range():
    db.ping(reconnect=True)
    start = request.args.get("start")
    end = request.args.get("end")
    sql = query_age_range_sql % (int(start), int(end))
    cursor.execute(sql)
    result = cursor.fetchone()
    result = json.dumps(result, ensure_ascii=False)

    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/user_age_static')
def get_age_static():
    birthday_sql = '''
    select t.bd ,count(*) as count from (
                select cast(left(birthday,4) as SIGNED INTEGER) as bd FROM keep_user_info 
                where birthday NOT LIKE '1900%' and birthday != 'None' and birthday not like '201%' ) 
              as t group by t.bd
    '''
    cursor.execute(birthday_sql)
    result = cursor.fetchall()

    tag_50s = '50s'
    tag_60s = '60s'
    tag_70s = '70s'
    tag_80s = '80s'
    tag_85s = '85s'
    tag_90s = '90s'
    tag_95s = '95s'
    tag_00s = '00s'
    map = {tag_50s: 0, tag_60s: 0, tag_70s: 0, tag_80s: 0, tag_85s: 0, tag_90s: 0, tag_95s: 0, tag_00s: 0}
    for item in result:
        bd = item['bd']
        count = item['count']
        if 1950 <= bd < 1960:
            map[tag_50s] = map[tag_50s] + count
        elif 1960 <= bd < 1970:
            map[tag_60s] = map[tag_60s] + count
        elif 1970 <= bd < 1980:
            map[tag_70s] = map[tag_70s] + count
        elif 1980 <= bd < 1985:
            map[tag_80s] = map[tag_80s] + count
        elif 1985 <= bd < 1990:
            map[tag_85s] = map[tag_85s] + count
        elif 1990 <= bd < 1995:
            map[tag_90s] = map[tag_90s] + count
        elif 1995 <= bd < 2000:
            map[tag_95s] = map[tag_95s] + count
        elif 2000 <= bd < 2010:
            map[tag_00s] = map[tag_00s] + count
    result = json.dumps(map, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/province_city_static/<province>')
def get_province_city_static(province):
    db.ping(reconnect=True)
    sql = '''
    select city,count(1) as count from keep_user_info where province = '%s' and length(city)>0 group by city
    '''
    cursor.execute(sql % province)
    result = cursor.fetchall()
    result = json.dumps(result, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/province_user_count', methods=['GET'])
def get_province_users_count():
    db.ping(reconnect=True)
    cursor.execute(query_province_users_count_sql)
    provincelist = cursor.fetchall()
    print(provincelist)
    result = json.dumps(provincelist, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/city_users_count', methods=['GET'])
def get_city_users_count():
    db.ping(reconnect=True)
    cursor.execute(query_city_users_count_sql)
    citylist = cursor.fetchall()
    print(citylist)
    result = json.dumps(citylist, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


class Total():
    pass


@app.route('/city_users/<citycode>')
def get_city_user(citycode):
    db.ping(reconnect=True)
    sql = query_city_users_sql % citycode
    cursor.execute(sql)
    result = cursor.fetchall()
    total = Total()
    total.key = citycode
    total.total = result[0]['count']
    return json.dumps(({citycode: total.total}), ensure_ascii=False)


@app.route('/province_users/<province>')
def get_province_user(province):
    db.ping(reconnect=True)
    sql = query_province_users_sql % province
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(({province: len(result)}), ensure_ascii=False)


@app.route('/userinfo/<id>', methods=['GET'])
def get_user_info(id):
    db.ping(reconnect=True)

    sql = query_user_info_sql % id
    row = cursor.execute(sql)
    db.commit()
    if row < 1:
        result = "查询失败，不存在该用户"
    else:
        result = cursor.fetchone()
        result = json.dumps(result, ensure_ascii=False)

    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


def makeResponse(result):
    rst = make_response(result)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return rst


@app.route('/wxusers/<page>/<count>', methods=['GET'])
def get_wx_user(page, count):
    page = int(page)
    count = int(count)
    sql = query_wx_user_list_sql % ((page - 1) * count, count)
    row = cursor.execute(sql)
    if row > 0:
        result = json.dumps(cursor.fetchall(), ensure_ascii=False)
    else:
        result = "没有更多用户"
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


@app.route('/users', methods=['GET'])
def get_user_list2():
    page = request.args.get("page")
    count = request.args.get("count")
    if page and count:
        page = int(page)
        count = int(count)
        sql = query_user_list_sql % ((page - 1) * count, count)
        row = cursor.execute(sql)
        if row > 0:
            result = json.dumps(cursor.fetchall(), ensure_ascii=False)
        else:
            result = "没有更多用户"
    else:
        result = "缺少参数"
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


@app.route('/users/<page>/<count>', methods=['GET'])
def get_user_list(page, count):
    page = int(page)
    count = int(count)
    sql = query_user_list_sql % ((page - 1) * count, count)
    row = cursor.execute(sql)
    if row > 0:
        result = json.dumps(cursor.fetchall(), ensure_ascii=False)
    else:
        result = "没有更多用户"
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


@app.route('/usertarins/<id>', methods=['GET'])
def get_user_train_list(id):
    db.ping(reconnect=True)
    sql = query_user_train_list_sql % id
    row = cursor.execute(sql)
    db.commit()
    if row > 0:
        result = json.dumps(cursor.fetchall(), ensure_ascii=False)
    else:
        result = "不存在该用户/该用户没有训练日志"
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


@app.route('/trains/<page>/<count>', methods=['GET'])
def get_top_trains(page, count):
    page = int(page)
    count = int(count)
    sql = query_top_train_list_sql % ((page - 1) * count, count)
    row = cursor.execute(sql)
    if row > 0:
        result = json.dumps(cursor.fetchall(), ensure_ascii=False)
    else:
        result = "没有更多用户"
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


@app.route('/trains/geo/<page>/<count>', methods=['GET'])
def get_geo_trains(page, count):
    page = int(page)
    count = int(count)
    sql = query_geo_train_list_sql % ((page - 1) * count, count)
    db.ping(reconnect=True)
    row = cursor.execute(sql)
    db.commit()
    if row > 0:
        result = json.dumps(cursor.fetchall(), ensure_ascii=False)
    else:
        result = "没有更多用户"
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return makeResponse(result)


import os


@app.route('/')
def main():
    return send_file('pie.html')


userDs = UserDatasource()



@app.route('/charts/user_country_data')
def get_country_user_data():
    pie = Pie('全国用户分布')
    map = userDs.get_country_user_data()
    labels = []
    data = []
    for k in map:
        labels.append(k)
        data.append(map[k])

    pie.add("", labels, data, is_label_show=True, legend_pos='bottom')
    fileName = 'pie.html'
    pie.render(fileName)

    return send_file(fileName)


@app.route('/charts/user_age_country_data')
def get_user_age_country_data():
    mapData = userDs.get_country_user_age_data()

    labels = []
    data = []
    total = 0
    for k in mapData:
        labels.append(k)
        count = mapData[k]
        data.append(count)
        total = total + count

    pie = Pie('全国%s用户年龄分布' % total)
    pie.add("", labels, data, is_label_show=True, legend_pos='bottom')
    fileName = 'user_age_country.html'
    pie.render(fileName)
    return send_file(fileName)


@app.route('/charts/bmi')
def get_country_user_bmi():
    result = userDs.get_country_user_bmi_data()
    below_low = '过轻'
    normal = '正常'
    over = '过重'
    fat = '肥胖'
    so_fat = '过度肥胖'
    labels = [below_low, normal, over, fat, so_fat]
    data = []
    mapData = {below_low: 0, normal: 0, over: 0, fat: 0, so_fat: 0}
    total = 0
    for k in result:
        count = k['count']
        bmi = float(k['bmi'])
        total = total + count
        if 0 < bmi < 18.5:
            mapData[below_low] = mapData[below_low] + count
        elif 18.5 <= bmi < 23.9:
            mapData[normal] = mapData[normal] + count
        elif 24 <= bmi < 27:
            mapData[over] = mapData[over] + count
        elif 27 <= bmi < 32:
            mapData[fat] = mapData[fat] + count
        elif bmi > 32:
            mapData[so_fat] = mapData[so_fat] + count
    for k in mapData:
        bmi = mapData[k]
        data.append(bmi)
    pie = Pie('全国%s用户bmi分布' % total)
    pie.add("", labels, data, is_label_show=True, legend_pos='bottom')
    fileName = 'user_bmi_country.html'
    pie.render(fileName)
    return send_file(fileName)


@app.route('/charts/user_age_data/city/<city>')
def get_city_user_age_data(city):
    pie = Pie('%s用户年龄分布' % city)
    mapData = userDs.get_city_user_age_data(city)

    labels = []
    data = []
    for k in mapData:
        labels.append(k)
        data.append(mapData[k])

    pie.add("", labels, data, is_label_show=True, legend_pos='bottom')
    fileName = 'user_age_city.html'
    pie.render(fileName)
    return send_file(fileName)


@app.route('/charts/user_age_data/province/<province>')
def get_province_user_age_data(province):
    pie = Pie('%s用户年龄分布' % province)
    mapData = userDs.get_province_user_age_data(province)

    labels = []
    data = []
    for k in mapData:
        labels.append(k)
        data.append(mapData[k])

    pie.add("", labels, data, is_label_show=True, legend_pos='bottom')
    fileName = 'user_age_province.html'
    pie.render(fileName)
    return send_file(fileName)


@app.route('/charts/user_city_data/province/<province>')
def get_province_city_user_data(province):
    pie = Pie('%s各城市用户分布' % province)
    listData = userDs.get_province_city_user_data(province)

    labels = []
    data = []
    for item in listData:
        labels.append(item['city'])
        data.append(item['count'])

    pie.add("", labels, data, is_label_show=True, legend_pos='bottom')
    fileName = 'user_city_data.html'
    pie.render(fileName)
    return send_file(fileName)


@app.route('/map/<province>')
def get_province_data(province):
    result = userDs.get_province_city_user_data(province)
    total = 0
    lables = []
    sizes = []
    for item in result:
        lables.append(item['city'])
        sizes.append(item['count'])
        total = total + item['count']
    max = numpy.max(sizes)
    min = numpy.min(sizes)
    map = Map("共爬取%s%s个用户" % (province, total), width=1200, height=600)
    map.add("%s 用户分布" % province, lables, sizes, visual_range=[min, max], is_visualmap=True, maptype=province[0:2],
            is_label_show=True, visual_text_color='#007')
    map.render('map.html')
    return send_file('map.html')


@app.route('/map')
def get_map_data():
    data = userDs.get_country_user_data()
    total = 0
    lables = []
    sizes = []
    for k in data:
        if len(k) > 0:
            try:
                index = k.index('省')
                if index > 0:
                    lables.append(k[0:index])
            except Exception as e:
                if k == '内蒙古自治区':
                    lables.append(k[0:3])
                else:
                    lables.append(k[0:2])

                pass

        sizes.append(data[k])
        total = total + data[k]

    max = numpy.max(sizes)
    min = numpy.min(sizes)
    map = Map("共爬取%s个用户" % total, width=1200, height=600)
    map.add("全国", lables, sizes, maptype='china', visual_range=[min, max], is_visualmap=True, is_label_show=True,
            visual_text_color='#007')
    map.render('map.html')
    return send_file('map.html')


@app.route("/new_user_year")
def get_user_year():
    result = userDs.get_user_join_time()
    labels = []
    count = []
    total = 0
    for year in result:
        labels.append(year)
        user_count = result[year]
        count.append(user_count)
        total = user_count + total

    line = Line("新增用户年份分布")
    line.add("新增用户年份分布", labels, count, mark_line=["average"])
    fileName = 'user_join_data_new_user_year.html'
    line.render(fileName)
    return send_file(fileName)

def get_user_month_line_data_of_year(year):
    result = userDs.get_user_month_of_year(year)
    labels = []
    count = []
    total = 0
    for month in result.keys():
        labels.append(month)
        user_count = result[month]
        count.append(user_count)
        total = user_count + total
    return labels, count, total
@app.route("/new_user_year_all")
def new_user_year_all():
    result_2015 = get_user_month_line_data_of_year(2015)
    result_2016 = get_user_month_line_data_of_year(2016)
    result_2017 = get_user_month_line_data_of_year(2017)
    result_2018 = get_user_month_line_data_of_year(2018)

    line = Line("新增用户趋势" )
    line.add('2015新增用户趋势', result_2015[0], result_2015[1], mark_line=["average"],is_smooth=True, mark_point=["max", "min"])
    line.add('2016新增用户趋势', result_2016[0], result_2016[1], mark_line=["average"],is_smooth=True, mark_point=["max", "min"])
    line.add('2017新增用户趋势', result_2017[0], result_2017[1], mark_line=["average"],is_smooth=True, mark_point=["max", "min"])
    line.add('2018新增用户趋势', result_2018[0], result_2018[1], mark_line=["average"],is_smooth=True, mark_point=["max", "min"])
    # bar.show_config()
    fileName = 'user_join_data.html'
    line.render(fileName)
    return send_file(fileName)
@app.route('/usermap')
def get_user_map():
    fileName = 'static/keepmap.html'
    return send_file(fileName)

@app.route('/user/duration')
def get_user_duration():
    result = userDs.count_user_duration()
    labels = []
    counts = []
    for k in result:
        count = result[k]
        labels.append(k)
        counts.append(count)
    pie = Pie('用户累计运动时长')
    pie.add("", labels, counts, is_label_show=True, legend_pos='bottom')
    fileName = 'user_duration_data.html'
    pie.render(fileName)
    return send_file(fileName)

@app.route('/user/distance')
def get_user_dis():
    result = userDs.count_user_dis()
    labels = []
    counts = []
    for k in result:
        count = result[k]
        labels.append(k)
        counts.append(count)
    pie = Pie('用户累计跑步距离')
    pie.add("", labels, counts, is_label_show=True, legend_pos='bottom')
    fileName = 'user_dis_data.html'
    pie.render(fileName)
    return send_file(fileName)


@app.route("/new_user_year/<year>")
def get_user_month_of_year(year):
    result = userDs.get_user_month_of_year(year)
    labels = []
    count = []
    total = 0
    for month in result.keys():
        labels.append(month)
        user_count = result[month]
        count.append(user_count)
        total = user_count + total
    line = Line("%s年新增用户月份分布" % year)
    line.add("%s年新增用户月份分布" % year, labels, count, mark_line=["average"],is_smooth=True, mark_point=["max", "min"])
    # bar.show_config()
    fileName = 'user_join_data.html'
    line.render(fileName)
    return send_file(fileName)


if __name__ == '__main__':
    app.run()
