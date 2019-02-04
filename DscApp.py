from flask import Flask
from flask import request

import pymysql.cursors
import requests
import json
from flask import make_response

from dsc_ds import DscDatasource

app = Flask(__name__, static_url_path='')

ds = DscDatasource()


@app.route("/get_user_list")
def query_user_list():
    start = request.args.get("start")
    end = request.args.get("end")
    result = json.dumps(ds.get_user_list(start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_from_company')
def get_user_list_from_company():
    start = request.args.get("start")
    end = request.args.get("end")
    keyword = request.args.get("keyword")
    result = json.dumps(ds.get_user_list_from_company(keyword, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_between_birthday')
def get_user_list_between_birthday():
    start = request.args.get("start")
    end = request.args.get("end")
    year = request.args.get("year")
    result = json.dumps(ds.get_user_list_between_birthday(year, start, end), ensure_ascii=False)
    print(len(result))
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_between_height')
def get_user_list_between_height():
    start = request.args.get("start")
    end = request.args.get("end")
    heightMin = request.args.get("heightMin")
    heightMax = request.args.get("heightMax")
    result = json.dumps(ds.get_user_list_between_height(heightMin, heightMax, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


# @app.route('/get_user_list_between_height')
# def get_user_list_between_height():
#     start = request.args.get("start")
#     end = request.args.get("end")
#     heightMin = request.args.get("heightMin")
#     heightMax = request.args.get("heightMax")
#     result = json.dumps(ds.get_user_list_between_height(heightMin, heightMax, start, end), ensure_ascii=False)
#     jsonp = request.args.get("jsonpCallback")
#     if jsonp:
#         return "%s(%s)" % (jsonp, result)
#     return make_response(result)


@app.route('/get_user_list_between_weight')
def get_user_list_between_weight():
    start = request.args.get("start")
    end = request.args.get("end")
    weightMin = request.args.get("weightMin")
    weightMax = request.args.get("weightMax")
    result = json.dumps(ds.get_user_list_between_weight(weightMin, weightMax, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_target_height')
def get_user_list_target_height():
    start = request.args.get("start")
    end = request.args.get("end")
    heightMin = request.args.get("heightMin")
    result = json.dumps(ds.get_user_list_target_height(heightMin, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_star_sign')
def get_user_list_star_sign():
    start = request.args.get("start")
    end = request.args.get("end")
    star_sign = request.args.get("star_sign")
    result = json.dumps(ds.get_user_list_star_sign(star_sign, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_education')
def get_user_list_with_education():
    start = request.args.get("start")
    end = request.args.get("end")
    education = request.args.get("education")
    result = json.dumps(ds.get_user_list_with_education(education, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_university')
def get_user_list_with_university():
    start = request.args.get("start")
    end = request.args.get("end")
    university = request.args.get("university")
    result = json.dumps(ds.get_user_list_with_university(university, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_user_list_with_area')
def get_user_list_with_area():
    start = request.args.get("start")
    end = request.args.get("end")
    area = request.args.get("area")
    result = json.dumps(ds.get_user_list_with_area(area, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)

@app.route('/get_user_list_with_area_and_birth')
def get_user_list_with_area_and_birth():
    start = request.args.get("start")
    end = request.args.get("end")
    area = request.args.get("area")
    birth = request.args.get("birth")
    result = json.dumps(ds.get_user_list_with_area_and_birth(area,birth, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)

@app.route('/get_user_list_with_hobby')
def get_user_list_with_hobby():
    start = request.args.get("start")
    end = request.args.get("end")
    hobby = request.args.get("hobby")
    result = json.dumps(ds.get_user_list_with_hobby(hobby, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)

@app.route('/get_user_list_with_company_and_birth')
def get_user_list_with_company_and_birth():
    start = request.args.get("start")
    end = request.args.get("end")
    company = request.args.get("company")
    birthday = request.args.get("birthday")
    result = json.dumps(ds.get_user_list_with_company_and_birth(company,birthday, start, end), ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


if __name__ == '__main__':
    app.run(port=5555)
