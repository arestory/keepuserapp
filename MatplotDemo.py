import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib
import time
from datasource import UserDatasource

userDs = UserDatasource()


# 查询某个省的城市用户分布
def show_province_city_user(province='广东省'):
    result = userDs.get_province_city_user_data(province)
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


# 展示全国用户分布
def show_country_pie():
    mapData = userDs.get_country_user_data()
    labels = []
    data = []
    for k in mapData.keys():
        if mapData[k] > 0:
            labels.append(k)
            data.append(mapData[k])
            print('%s人数：%s' % (k, mapData[k]))

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


def __show_all_province():
    result = userDs.get_province_list()
    for item in result:
        time.sleep(1)
        show_province_user_age_pie(item['province'])
    pass


# show_all_province()

# 少数民族
def show_shaoshu():
    result = userDs.get_shaoshu_minzu_data()
    labels = []
    data = []
    total = 0
    for item in result:
        province = item['province']
        count = item['count']
        total = total + count
        if count >= 5:
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
    result = userDs.get_zhixia_city_list()
    labels = []
    data = []
    total = 0
    for item in result:
        province = item['province']
        count = item['count']
        total = total + count
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
    map = userDs.get_city_user_age_data(city)
    labels = []
    data = []
    for k in map.keys():
        labels.append(k)
        data.append(map[k])

    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange', 'yellow', 'red', 'pink'
    explode = 0, 0, 0, 0, 0.1, 0, 0

    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)
    pie = plt.pie(data, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=40,
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
    map = userDs.get_province_user_age_data(province)
    labels =[]
    data = []

    for k in map.keys():
        labels.append(k)
        data.append(map[k])
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange', 'yellow', 'red', 'pink'
    explode = 0, 0, 0, 0, 0.1, 0, 0

    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)
    pie = plt.pie(data, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=40,
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
    map = userDs.get_country_user_age_data()
    data =[]
    labels =[]
    for k in map:
        labels.append(k)
        data.append(map[k])
    colors = 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange', 'yellow', 'red', 'pink'
    explode = 0, 0, 0, 0, 0.1, 0, 0

    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)
    pie = plt.pie(data, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=40,
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


# show_user_city()
