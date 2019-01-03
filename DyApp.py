from flask import Flask
from flask import request
import requests
import urllib.parse
from lxml import etree
from bs4 import BeautifulSoup

from flask import make_response
import json

app = Flask(__name__, static_url_path='')

rootUrl = "https://www.dytt8.net"

dyTag = "/html/gndy/"

chinaDy = dyTag + "china/"

rihanDy = dyTag + "rihan/"

oumeiDy = dyTag + "oumei/"

pageOne = "index.html"

tvTag = "/html/tv/"

hytv = tvTag + "hytv/"

rihantv = tvTag + "rihantv/"

oumeitv = tvTag + "oumeitv/"


# 搜索
@app.route("/search/<type>/<keyword>")
def search(type, keyword):
    url = ""
    typeid = 0
    if type == 'tv':
        typeid = 2
        pass
    elif type == "movie":
        typeid = 1
        pass
    url = "http://s.ygdy8.com/plus/so.php?typeid=%s&keyword=%s" % (typeid, urllib.parse.quote(keyword.encode('gbk')))
    r = requests.get(url)
    decode = requests.utils.get_encodings_from_content(r.text)
    print(decode)
    r.encoding = "GBK"
    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("div", class_="co_content8")
    bList = root.find_all("b")
    resultJson = {}
    if typeid == 2:
        map = []
        for b in bList:
            a = b.find_all('a')[1]
            href = a.attrs['href']
            name = a.get_text()
            obj = {"name": name, "href": href}
            map.append(obj)
        x = soup.find_all("div", class_="x")[1]
        x = x.find_all('a')
        resultJson = {'list': map}

        pass
    elif typeid == 1:
        map = []
        for b in bList:
            a = b.find_all('a')[0]
            href = a.attrs['href']
            name = a.get_text()
            if not name.__contains__('下载网站APP') and not name.__contains__('点这里返回首页下载'):
                obj = {"name": name, "href": href}
                map.append(obj)
        x = soup.find_all("div", class_="x")[1]
        x = x.find_all('a')
        resultJson = {'list': map}

    result = json.dumps(resultJson, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


@app.route('/get_zhongyi')
def get_zhongyi():

    # 页码
    pageIndex = request.args.get("index")
    if not pageIndex:
        pageIndex = "index.html"
    url = "https://www.dytt8.net/html/zongyi2013/" + pageIndex
    r = requests.get(url)
    decode = requests.utils.get_encodings_from_content(r.text)
    print(decode)
    r.encoding = "GBK"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("div", class_="co_content8")
    bList = root.find_all("b")
    map = []
    for b in bList:
        a = b.find_all('a')[1]
        href = a.attrs['href']
        name = a.get_text()
        obj = {"name": name, "href": href}
        map.append(obj)
    x = soup.find_all("div", class_="x")[1]
    x = x.find_all('a')
    resultJson = {'list': map}
    for a in x:
        text = a.get_text()
        if text == '下一页':
            href = a['href']
            print(href)
            print(text)
            resultJson['nextpage'] = href
    result = json.dumps(resultJson, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)

# 获取电影列表
@app.route('/get_movies')
def get_movie_list():
    # 地区
    area = request.args.get("area")
    url = ""
    if area == "china":
        url = rootUrl + chinaDy
    elif area == "rihan":
        url = rootUrl + rihanDy
    elif area == "oumei":
        url = rootUrl + oumeiDy
    else:
        return "area 参数有误"
    # 页码
    pageIndex = request.args.get("index")
    url = url + pageIndex
    r = requests.get(url)
    decode = requests.utils.get_encodings_from_content(r.text)
    print(decode)
    r.encoding = "GBK"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("div", class_="co_content8")
    bList = root.find_all("b")
    map = []
    for b in bList:
        a = b.find_all('a')[1]
        href = a.attrs['href']
        name = a.get_text()
        obj = {"name": name, "href": href}
        map.append(obj)
    x = soup.find_all("div", class_="x")[1]
    x = x.find_all('a')
    resultJson = {'list': map}
    for a in x:
        text = a.get_text()
        if text == '下一页':
            href = a['href']
            print(href)
            print(text)
            resultJson['nextpage'] = href
    result = json.dumps(resultJson, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


# 获取电视剧列表
@app.route('/get_tvs')
def get_tv_list():
    area = request.args.get("area")
    url = ""
    if area == "china":
        url = rootUrl + hytv
    elif area == "rihan":
        url = rootUrl + rihantv
    elif area == "oumei":
        url = rootUrl + oumeitv
    else:
        return "area 参数有误"
    pageIndex = request.args.get("index")
    url = url + pageIndex
    r = requests.get(url)
    decode = requests.utils.get_encodings_from_content(r.text)
    print(decode)
    r.encoding = "GBK"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("div", class_="co_content8")
    bList = root.find_all("b")
    map = []
    for b in bList:
        a = b.find_all('a')[0]
        href = a.attrs['href']
        name = a.get_text()
        obj = {"name": name, "href": href}
        map.append(obj)
    x = soup.find_all("div", class_="x")[1]
    x = x.find_all('a')
    resultJson = {'list': map}
    for a in x:
        text = a.get_text()
        if text == '下一页':
            href = a['href']
            print(href)
            print(text)
            resultJson['nextpage'] = href
    result = json.dumps(resultJson, ensure_ascii=False)
    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


# 影视想去
@app.route("/movie/detail")
def get_video_detail():
    pageUrl = request.args.get("url")
    url = rootUrl + pageUrl
    r = requests.get(url)
    decode = requests.utils.get_encodings_from_content(r.text)
    print(decode)
    r.encoding = "GBK"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find(id="Zoom")
    if not root:
        url = "https://www.ygdy8.com/" + pageUrl
        r = requests.get(url)
        decode = requests.utils.get_encodings_from_content(r.text)
        print(decode)
        r.encoding = "GBK"
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        root = soup.find(id="Zoom")

    coverImg = root.find('img')['src']
    trList = root.find_all('tr')
    downloadList = []
    for item in trList:
        a = item.find('td').find('a')
        href = a['href']
        if len(href) > 0 and (href.__contains__('http') or href.__contains__('ftp') or href.__contains__('magnet')):
            downloadList.append(href)
        print(href)
    pList = root.find_all('p')
    spanList = root.find_all('span')
    desc = []
    if len(pList) > 0:
        p = pList[0]
        contents = p.contents
        if len(contents) == 1:
            span = spanList[0]
            pList = span.find_all('p')
            if len(pList) > 0:
                for item in pList:
                    content = item.contents[0]
                    try:
                        if len(content) > 0:
                            desc.append(content.strip())
                    except Exception as e:
                        print(e)
                        pass
        else:
            try:
                for item in contents:
                    if type(item).__name__ == 'NavigableString' and len(item) > 0:
                        item = item.strip()
                        if len(item) > 0:
                            desc.append(item)
            except Exception as e:
                print(e)

        pass
    actressIndex = 0
    descIndex = 0
    goalIndex = 0
    actressArr = ""
    infoList = []
    for index, item in enumerate(desc):
        if item.__contains__('主') and (item.__contains__('演')):
            actressIndex = index
        if item.__contains__('简') and (item.__contains__('介')):
            descIndex = index
        if item.__contains__('获奖情况'):
            goalIndex = index

    infoList = []
    for index, item in enumerate(desc):
        if (actressIndex != 0 and descIndex != 0) and actressIndex < index < descIndex:
            infoList[len(infoList) - 1] = infoList[len(infoList) - 1] + "," + item.split(" ")[0]
        elif goalIndex != 0 and index >= goalIndex:
            if index == goalIndex:
                infoList.append(item.replace("◎", "").replace("　　", ""))
            else:
                infoList[len(infoList) - 1] = infoList[len(infoList) - 1] + "\n" + item
        elif descIndex != 0 and index > descIndex:
            infoList[len(infoList) - 1] = infoList[len(infoList) - 1] + "\n" + item
        else:
            infoList.append(item.replace("◎", "").replace("　　", "").replace("　", ":"))
        pass
    result = {"coverImg": coverImg, "downloadList": downloadList, "desc": infoList}
    result = json.dumps(result, ensure_ascii=False)

    jsonp = request.args.get("jsonpCallback")
    if jsonp:
        return "%s(%s)" % (jsonp, result)
    return make_response(result)


if __name__ == '__main__':
    app.run(port=8585)
