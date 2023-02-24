from lxml.html import tostring
import re


def get_basic_data(movie):
    # 电影信息
    movie_info = movie.xpath('div[@class="info"]')[0]
    movie_bd = movie_info.xpath('div[@class="bd"]')[0]
    movie_credits = movie_bd.xpath('p')[0]
    movie_star_info = movie_bd.xpath('div[@class="star"]')[0]
    movie_quote = movie_bd.xpath('p[@class="quote"]')

    movie_div = tostring(movie_info, encoding="utf-8").decode("utf-8")

    # 获取电影名
    movie_title = re.findall(
        r'<span class="title">(.*)</span>', movie_div)
    name1 = movie_title[0].strip()
    if len(movie_title) > 1:
        name2 = "".join(movie_title[1].strip()[1:].split())
    else:
        name2 = '-'

    # 电影评分
    score = float(movie_star_info.xpath(
        'span[@class="rating_num"]/text()')[0])

    # 评价人数
    comment = int(movie_star_info.xpath(
        'span')[-1].xpath('text()')[0][:-3])  # ...人评价\

    # 电影语录
    if len(movie_quote) > 0:
        quote_str = movie_quote[0].xpath('span/text()')[0]
    else:
        quote_str = ''

    # 电影详情URL
    page_url = re.findall(
        r'<a href="(.*)" class="">', movie_div)[0]

    return name1, name2, score, comment, quote_str, page_url
