import lxml.html
import re


def get_detail_data(movie_html: str):
    # print(movie_html)

    _selector = lxml.html.fromstring(movie_html)
    movie_page_divs = _selector.xpath('//div[@id="info"]')[0]
    # print(movie_page_divs)

    '''
    例:
    
    类型: 剧情 / 犯罪
    制片国家/地区: 美国
    语言: 英语
    上映日期: 1994-09-10(多伦多电影节) / 1994-10-14(美国)
    片长: 142分钟
    又名: 月黑高飞(港) / 刺激1995(台) / 地狱诺言 / 铁窗岁月 / 消香克的救赎
    IMDb: tt0111161
    '''

    info_str = _selector.xpath('//div[@id="info"]')[0].xpath('string(.)').strip()
    
    type = re.findall(r'类型: (.*)', info_str)[0].split(' / ')
    place = re.findall(r'制片国家/地区: (.*)', info_str)[0].split(' / ')
    lang = re.findall(r'语言: (.*)', info_str)[0].split(' / ')
    year = int(re.findall(r'上映日期: (....)', info_str)[0])
    length = int(re.findall(r'片长: (.*?)分钟', info_str)[0])

    # print(type, place, lang, year, length)

    movie_attrs = movie_page_divs.xpath('//span[@class="attrs"]')
    director = movie_attrs[0].xpath("a/text()")
    if len(movie_attrs) < 3:
        actor = ''
    else:
        actor = movie_attrs[2].xpath("a/text()")
    # print(director)
    # print(actor)

    return director, actor, type, place, lang, year, length
 