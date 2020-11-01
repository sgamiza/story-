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
}


def get_file_name2(headers):
    if 'Content-Location' in headers:
        filename = headers['Content-Location'].rsplit('/',1)[1]
        return filename

def getTags_and_download():
    url = 'http://www.goodkejian.com/ertonggushi.htm'
    # resp = session.get(url=url, headers=headers, params=params)
    resp = session.get(url=url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    item_list = soup.find_all(name='div',attrs={'class':'down16x16'})
    for item in item_list:
        a = item.find(name='a')  
        a_href = item.a['href']  
        download_href(a_href)


def download_href(href):
    r = requests.get(href, stream=True)
    file_name = get_file_name2(r.headers)
    with open(rf"C:\Users\mi\Downloads\taotao\new\{file_name}", "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)


if __name__ == '__main__':
    getTags_and_download()
