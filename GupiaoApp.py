from flask import Flask
from flask import request
from flask import make_response
import json,time

from GupiaoDataSource import GupiaoDs

app = Flask(__name__, static_url_path='')
ds = GupiaoDs()


@app.route("/addStock")
def add_stock():
    code = request.args.get("id")
    name = request.args.get("name")
    vol = request.args.get("vol")
    create_time = request.args.get("create_time")
    if code and name and vol:
        result = ds.add_stock(code, name, vol,create_time)
        if result == -1:
            map_result = {'code': -1, 'msg': '添加失败'}

        else:
            map_result = {'code': 200, 'msg': '添加成功'}

    else:
        map_result = {'code': -100, 'msg': '缺少参数，请检查'}
    result = json.dumps(map_result, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/deleteTodayAddStock')
def delete_today_add_stock():
    code = request.args.get('id')
    ds.delete_today_add_stock(code)
    map_result = {'code': 200, 'msg': '删除成功'}
    result = json.dumps(map_result, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/queryTodayStocks')
def query_today_stocks():
    date = request.args.get('date')
    stock_list = ds.query_today_add_stocks(date)
    result = json.dumps(stock_list, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route("/queryStocks")
def query_stock_list():
    stock_list = ds.query_yesterday_stock()
    result = json.dumps(stock_list, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/add_stock_list')
def add_stock_list():
    stocks = json.loads(request.args.get("list"))
    print(stocks)
    create_time = request.args.get("create_time")
    if not create_time:
        create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    for stock in stocks:
        # 添加到数据库
        ds.add_stock(stock['code'], stock['name'], stock['vol_on_up'],create_time)

    result = json.dumps({'code': 200, 'msg': '成功'}, ensure_ascii=False)

    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/query925stocks')
def query925stocks():
    # 获取昨天记录的股票数据
    stock_list = ds.query_yesterday_stock()
    result = []
    jsonp = request.args.get("jsonpCallback")

    if len(stock_list)>0:
        for stock in stock_list:
            # 查看数据是否已经存在记录
            detail = ds.get_gp_info_on925_table(stock['id'])
            if not detail:
                detail = ds.get_gp_info_on_time(stock['id'])
            if detail:
                vol = stock['vol_on_up']
                call_auction = detail['call_auction']
                percent = call_auction / (vol*100)
                result_map = {'id': stock['id'], 'name': stock['name'], 'create_time': detail['create_time'], 'vol_on_up': vol,
                              'call_auction': call_auction, 'percent': round(percent, 2)}
                result.append(result_map)

        result = json.dumps(result, ensure_ascii=False)
    else:
        result = json.dumps([], ensure_ascii=False)
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/queryStockWithCondition')
def judge_stock_with_condition():
    code = request.args.get("id")
    if code:
        item_on_sql = ds.get_gp_info(code)
        item_on_time = ds.get_gp_info_on_time(code)
        print(item_on_sql)
        print(item_on_time)

        vol_on_up = item_on_sql['vol_on_up']
        call_auction = item_on_time['call_auction']
        percent = call_auction / (vol_on_up*100)
        print(percent)
        map = {'id': code, 'name': item_on_sql['name'], 'vol_on_up': vol_on_up, 'call_auction': call_auction,
               'percent': percent}
        # map = {'item_on_sql': item_on_sql, 'item_on_time': item_on_time}
    else:
        map = {'code': -1, 'msg': '缺少股票代码'}
    result = json.dumps(map, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


app.run(port=2000)
