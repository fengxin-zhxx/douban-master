import requests
import lxml.html
import pandas as pd
import time
import os


from movie_detail import get_detail_data
from movie_basic import get_basic_data
from database import db_store, db_store_2, csv_store
from lxml.html import tostring
import re

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
    time.sleep(3)
    print('sleeping...')
    return requests.get(url, headers=headers).content.decode(encoding='utf-8')


def get_data(url: str):
    movies_data = []
    for i in range(10):
        print(i)
        start = i * 25

        _url = get_url(url, start=start)

        if local_test:
            # 使用本地文件
            html = open("./html/from_" + str(start + 1) + ".html", "r", encoding='utf-8').read()
        else:
            # 使用网络请求
            html = get_html(_url)
            time.sleep(0.5)
            with open("./html/from_" + str(start + 1) + ".html", 'w+', encoding='utf-8') as f:
                f.write(html.encode('utf-8').decode('utf-8'))

        selector = lxml.html.fromstring(html)
        movie_divs = selector.xpath('//div[@class="item"]')

        for movie in movie_divs:
            name1, name2, score, comment, quote_str, page_url = get_basic_data(
                movie)

            # 详情页内容爬取
            if local_test:
                # 使用本地文件
                movie_html = open("./html/" + name1 + ".html", "r", encoding='utf-8').read()
            else:
                # 使用网络请求
                movie_html = get_html(page_url)
                time.sleep(0.5)
                with open("./html/" + name1 + ".html", 'w+', encoding='utf-8') as f:
                    f.write(movie_html.encode('utf-8').decode('utf-8'))

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


get_data(url).to_csv("result.csv")

url_maoyan = 'https://piaofang.maoyan.com/rankings/year'
url_prefix = 'https://www.douban.com/search?cat=1002&q='

def get_search_url(text):
    return url_prefix + text

def get_data_douban(name : str, html : str):
        
    movies = lxml.html.fromstring(html)
    score = movies.xpath('/html/body/div[3]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/span[2]/text()')[0]
    comment = movies.xpath('/html/body/div[3]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/span[3]/text()')[0]
    comment = int(comment[1:-4])
    h3 = movies.xpath('/html/body/div[3]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3')
    h3 = tostring(h3[0], encoding="utf-8").decode("utf-8")
    page_url = re.findall(r'<a href="(.*)" target=', h3)[0]
    return score, comment, page_url


def get_data_maoyan(html : str):
    if local_test:
        with open("./html/maoyan.html", 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        html = get_html(url)
        with open("./html/maoyan.html", 'w+', encoding='utf-8') as f:
            f.write(html.encode('utf-8').decode('utf-8'))
            
    movies = lxml.html.fromstring(html)
    rank_list = movies.xpath('//div[@id="ranks-list"]')[0]
    rows = rank_list.xpath('ul[@class="row"]')
    all_data = []
    count = 0
    for row in rows:
        li = row.xpath('li')
        name_date = li[1].xpath('p')
        name = name_date[0].xpath('text()')[0]
        date = name_date[1].xpath('text()')[0][:-3]
        money = int(li[2].xpath('text()')[0])
        avg_money = float(li[3].xpath('text()')[0])
        avg_people = int(li[4].xpath('text()')[0])
        try:
            search_file = "./html/search"+ name + ".html"
            if local_test and os.path.isfile(search_file):
                with open(search_file , 'r', encoding='utf-8') as f:
                    html = f.read()
            else:
                html = get_html(get_search_url('[电影]' + name))
                with open(search_file, 'w+', encoding='utf-8') as f:
                    f.write(html.encode('utf-8').decode('utf-8'))
                
            score, comment, page_url = get_data_douban(name, html)
            file_name = "./html/" + name + ".html"
            # 详情页内容爬取
            if local_test and os.path.isfile(file_name):
                # 使用本地文件
                movie_html = open(file_name, "r", encoding='utf-8').read()
            else:
                # 使用网络请求
                movie_html = get_html(page_url)
                with open("./html/" + name + ".html", 'w+', encoding='utf-8') as f:
                    f.write(movie_html.encode('utf-8').decode('utf-8'))
                    
            director, actor, type, place, lang, year, length = get_detail_data(movie_html)
            data = [name, date, money, avg_money, avg_people, score, comment, director, actor, type, place, lang, length]
            # print(data)
            all_data.append(data)
            db_store_2(data)
            count += 1
            if count % 50 == 0:
                print("No." + str(count + 1) + " Done :" + name)
        except Exception as e:
            print("Error on searching " + name + '\n' + str(e))
            # os.remove(search_file)
            # os.remove(file_name)
        # break

    all_data = pd.DataFrame(all_data, columns=['电影名', '上映日期', '票房(万元)', '平均票价', '场均人数', '豆瓣评分', '豆瓣评论数',
                                    '导演', '演员', '类型', '地区', '语言', '时长'])
    
    all_data.to_csv('猫眼_豆瓣.csv')

    # return 


result = get_data_maoyan(url_maoyan)