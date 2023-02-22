import lxml.html
import requests


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

def get_html(url: str) -> str:
    return requests.get(url, headers=headers).content.decode(encoding='utf-8')


url = 'https://www.douban.com/search?q=满江红'

html = get_html(url)

with open('manjianghong.html', 'w+', encoding='utf-8') as f:
    f.write(html.encode('utf-8').decode('utf-8'))

# with open('manjianghong.html', 'r', encoding='utf-8') as f:
#     html = f.read()
    
print(html)