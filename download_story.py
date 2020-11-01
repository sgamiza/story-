import re
import requests
import random
import time
import os
import json
from PIL import Image
import re
import requests
from bs4 import BeautifulSoup


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'

session = requests.session()



headers = {
    'User-Agent': user_agent,
    # 'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F',
}

params = {
    'appid': '133',
}


# 获取现在文件的文件名称
def get_file_name(url, headers):
    filename = ''
    if 'Content-Disposition' in headers and headers['Content-Disposition']:
        disposition_split = headers['Content-Disposition'].split(';')
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith('filename='):
                file_name = disposition_split[1].split('=')
                if len(file_name) > 1:
                    filename = unquote(file_name[1])
    if not filename and os.path.basename(url):
        filename = os.path.basename(url).split("?")[0]
    if not filename:
        return time.time()
    return filename


# 获取现在文件的文件名称
def get_file_name2(headers):
    if 'Content-Location' in headers:
        filename = headers['Content-Location'].rsplit('/',1)[1]
        return filename



# 查找需要的div (正则)
# 还嵌套了子的div的内容无法用这个函数
def getTags(html):
    reg = r'<div class="result_info">([\s\S]+?)</div>'
    pattern = re.compile(reg)
    tags = re.findall(pattern, html)
    return tags



# 查找需要的div (soup)
def getTags_and_download():
    url = 'http://www.goodkejian.com/ertonggushi.htm'
    # resp = session.get(url=url, headers=headers, params=params)
    resp = session.get(url=url, headers=headers)

    soup = BeautifulSoup(resp.text, 'html.parser')
    # [标签对象,标签对象]
    item_list = soup.find_all(name='div',attrs={'class':'down16x16'})
    for item in item_list:
        a = item.find(name='a')  # 查找div下面的a标签  <class 'bs4.element.Tag'>
        a_href = item.a['href']  # div下面的所有a标签的href属性 <class 'str'>
        download_href(a_href)


def download_href(href):
    r = requests.get(href, stream=True)
    file_name = get_file_name2(r.headers)
    with open(rf"C:\Users\mi\Downloads\taotao\new\{file_name}", "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)


def download_href2(href):
    from contextlib import closing
    r = requests.get(href, stream=True)
    file_name = get_file_name2(r.headers)
    with closing(r) as r1:
    # 在此处理响应。
    for i in r1.iter_content():
        print(i)


if __name__ == '__main__':
    # test start
    # resp = session.get('http://www.goodkejian.com/down.asp?id=59719&sid=2', headers=headers)
    # get_file_name2(resp.headers)
    # test end

    getTags_and_download()
