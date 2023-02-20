import requests
import lxml.html
import pandas as pd
import time


from movie_detail import get_detail_data
from movie_basic import get_basic_data
from database import db_store, csv_store

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1"
}

# 是否使用本地文件测试
local_test = True


def get_url(url: str, start: int) -> str:
    return url.replace('start=0', 'start=' + str(start))


def get_html(url: str) -> str:
    return requests.get(url, headers=headers).content.decode(encoding='utf-8')


def get_data(url: str):
    movies_data = []
    for i in range(10):
        print(i)
        start = i * 25

        _url = get_url(url, start=start)

        if local_test:
            # 使用本地文件
            html = open("./html/from_" + str(start + 1) + ".html", "r").read()
        else:
            # 使用网络请求
            html = get_html(_url)
            time.sleep(0.5)
            with open("./html/from_" + str(start + 1) + ".html", 'w+') as f:
                f.write(html)

        selector = lxml.html.fromstring(html)
        movie_divs = selector.xpath('//div[@class="item"]')

        for movie in movie_divs:
            name1, name2, score, comment, quote_str, page_url = get_basic_data(
                movie)

            # 详情页内容爬取
            if local_test:
                # 使用本地文件
                movie_html = open("./html/" + name1 + ".html", "r").read()
            else:
                # 使用网络请求
                movie_html = get_html(page_url)
                time.sleep(0.5)
                with open("./html/" + name1 + ".html", 'w+') as f:
                    f.write(movie_html)

            # 详细信息
            director, actor, type, place, lang, year, length = get_detail_data(
                movie_html)

            movie_data = [name1, name2, score, comment, quote_str,
                          page_url, director, actor, type, place, lang, year, length]

            # 存储到数据库
            db_store(movie_data)

            # print(movie_data)

            movies_data.append(movie_data)

    csv_store()
    movies_data = pd.DataFrame(movies_data, columns=[
        '中文名', '外文名', '评分', '评价人数', '电影语录',  '详情URL', '导演', '主演', '类型', '地区', '语言', '上映年份', '时长'])

    return movies_data


url = "https://movie.douban.com/top250?start=0&filter="

# get_data(url)
get_data(url).to_csv("result.csv")
