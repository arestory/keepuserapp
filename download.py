from urllib import request
def _schedule(a, b, c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b * 1.0 / c
    if per > 100:
        per = 100
    if per==100:

        print('下载完毕')


def download_file(url, path):
     print("开始下载：",url)
     request.urlretrieve(url, path, _schedule)
