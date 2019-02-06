from flask import Flask
from flask import request

import pymysql.cursors
import requests
import json
from flask import make_response

from dsc_ds import DscDatasource

app = Flask(__name__, static_url_path='')

ds = DscDatasource()


def query_user_gallery(token, userId):
    headers = {'app-version': '3.5.0', 'Content-Type': "application/json", 'meet-token': token}
    lastId = request.args.get('lastId')
    if lastId == '0':
        url = 'https://dscapp.dscun.com/api/feeds/user/%s/feeds_id/0/count/10' % userId
    else:
        url = 'https://dscapp.dscun.com/api/feeds/user/%s/feeds_id/%s/count/-10' % (userId, lastId)
    r = requests.get(url, headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    data = js['data']
    result = {'code': js['code'], 'msg': js['msg'], 'data': []}
    if result['code'] == 10003:
        return result
    if data != "{}":
        if len(data['feeds']) > 0:
            items = []
            for item in data['feeds']:
                map = {'feeds_id': item['feeds_id'], 'feeds_data': item['feeds_data'], 'height': item['height'],
                       'width': item['width'], 'image': item['image'], 'insert_date': item['insert_date']}
                items.append(map)
                pass
            result['data'] = items
    return result


def interest_some(token, userId):
    headers = {'app-version': '3.5.0', 'meet-token': token}
    url = 'https://dscapp.dscun.com/api/user/interest/%s' % userId
    print(url)
    r = requests.post(url, headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    data = js['data']
    if js['code'] == 0:
        result = {'code': js['code'], 'msg': js['msg'], 'data': '关注成功，请打开APP查看'}
    else:
        result = {'code': js['code'], 'msg': js['msg'], 'data': '关注失败'}

    return result


@app.route('/interest')
def interest_someone():
    token = request.args.get('token')
    userId = request.args.get('userId')
    result = interest_some(token, userId)

    if result['code'] == 10003:
        # 重新登录
        login_result = login_oper('15920419761', 'yuwenque')
        new_token = login_result['data']['token']
        result = interest_some(new_token, userId)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_gallery')
def get_user_gallery():
    token = request.args.get('token')
    userId = request.args.get('userId')

    result = query_user_gallery(token, userId)
    jsonp = request.args.get("jsonpCallback")

    if result['code'] == 10003:
        # 重新登录
        login_result = login_oper('15920419761', 'yuwenque')
        new_token = login_result['data']['token']
        result = query_user_gallery(new_token, userId)

    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


def login_oper(name, password):
    params = {"tel": name,
              "password": password}
    headers = {'app-version': '3.5.0', 'Content-Type': "application/json"}
    r = requests.post('https://dscapp.dscun.com/api/session', json=params, headers=headers)
    content = r.content.decode('utf-8')
    js = json.loads(content)
    return js


@app.route('/login')
def login():
    name = request.args.get('name')
    pwd = request.args.get('password')
    js = login_oper(name, pwd)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, js)
    return make_response(js)


@app.route('/get_user_info')
def get_user_info():
    userId = request.args.get('id')
    result = json.dumps(ds.get_user_info(userId), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route("/get_user_list")
def query_user_list():
    start = request.args.get("start")
    count = request.args.get("count")
    result = json.dumps(ds.get_user_list(start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_from_company')
def get_user_list_from_company():
    start = request.args.get("start")
    count = request.args.get("count")
    keyword = request.args.get("keyword")
    result = json.dumps(ds.get_user_list_from_company(keyword, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_between_birthday')
def get_user_list_between_birthday():
    start = request.args.get("start")
    count = request.args.get("count")
    year = request.args.get("year")
    result = json.dumps(ds.get_user_list_between_birthday(year, start, count), ensure_ascii=False)
    print(len(result))
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_between_height')
def get_user_list_between_height():
    start = request.args.get("start")
    count = request.args.get("count")
    heightMin = request.args.get("heightMin")
    heightMax = request.args.get("heightMax")
    result = json.dumps(ds.get_user_list_between_height(heightMin, heightMax, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


# @app.route('/get_user_list_between_height')
# def get_user_list_between_height():
#     start = request.args.get("start")
#     count = request.args.get("count")
#     heightMin = request.args.get("heightMin")
#     heightMax = request.args.get("heightMax")
#     result = json.dumps(ds.get_user_list_between_height(heightMin, heightMax, start, count), ensure_ascii=False)
#     jsonp = request.args.get("jsonpCallback")
#     if jsonp:
#         return "%s(%s)" % (jsonp, result)
#     return make_response(result)


@app.route('/get_user_list_between_weight')
def get_user_list_between_weight():
    start = request.args.get("start")
    count = request.args.get("count")
    weightMin = request.args.get("weightMin")
    weightMax = request.args.get("weightMax")
    result = json.dumps(ds.get_user_list_between_weight(weightMin, weightMax, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_target_height')
def get_user_list_target_height():
    start = request.args.get("start")
    count = request.args.get("count")
    heightMin = request.args.get("heightMin")
    result = json.dumps(ds.get_user_list_target_height(heightMin, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_star_sign')
def get_user_list_star_sign():
    start = request.args.get("start")
    count = request.args.get("count")
    star_sign = request.args.get("star_sign")
    result = json.dumps(ds.get_user_list_star_sign(star_sign, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_education')
def get_user_list_with_education():
    start = request.args.get("start")
    count = request.args.get("count")
    education = request.args.get("education")
    result = json.dumps(ds.get_user_list_with_education(education, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_university')
def get_user_list_with_university():
    start = request.args.get("start")
    count = request.args.get("count")
    university = request.args.get("university")
    result = json.dumps(ds.get_user_list_with_university(university, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_area')
def get_user_list_with_area():
    start = request.args.get("start")
    count = request.args.get("count")
    area = request.args.get("area")
    result = json.dumps(ds.get_user_list_with_area(area, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_area_and_birth')
def get_user_list_with_area_and_birth():
    start = request.args.get("start")
    count = request.args.get("count")
    area = request.args.get("area")
    birth = request.args.get("birth")
    result = json.dumps(ds.get_user_list_with_area_and_birth(area, birth, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_hobby')
def get_user_list_with_hobby():
    start = request.args.get("start")
    count = request.args.get("count")
    hobby = request.args.get("hobby")
    result = json.dumps(ds.get_user_list_with_hobby(hobby, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_company_and_birth')
def get_user_list_with_company_and_birth():
    start = request.args.get("start")
    count = request.args.get("count")
    company = request.args.get("company")
    birthday = request.args.get("birthday")
    result = json.dumps(ds.get_user_list_with_company_and_birth(company, birthday, start, count), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


if __name__ == '__main__':
    app.run(port=5555)
