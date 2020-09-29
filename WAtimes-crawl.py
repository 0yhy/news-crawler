import requests
import re
import constant
from bs4 import BeautifulSoup


news_links = set()
old_links = set()


def initiate_old_links():
    with open('data/WAtimes/links.txt', 'r') as file_object:
        for url in file_object:
            old_links.add(url)
    # print(old_links)


def get_news_links(sub_url):
    # 下载新闻页html
    news_url = constant.WA_TIMES_URL + sub_url
    html = requests.get(news_url).text

    # 提取链接
    links = re.findall(r'href=[\'"]?(.*?)[\'"\s]', html)
    for link in links:
        if link.startswith('/news/20') and constant.WA_TIMES_URL + link + '\n' not in old_links:
            news_links.add(constant.WA_TIMES_URL + link)
    print(news_links)


# 根据链接数组获取每一页的HTML并解析
def get_news(links):
    for link in links:
        html = requests.get(link).text
        parseHtml(html)


# 解析每一页的HTML
def parseHtml(html):
    bs = BeautifulSoup(html, features="html.parser")
    # 提取标题
    news_title = bs.h1.string.strip()
    news_content_list = bs.select(".bigtext > p")
    news_content = ''
    for p in news_content_list:
        news_content = news_content + p.text + '\n'
    print(news_title)
    news = news_title + '\n' + news_content + '\n\n'
    # 如果内容包含"China"或"Chinese"
    if('China' in news or 'Chinese' in news):
        save_news_to_file(news)


# 将内容存到文件中
def save_news_to_file(html):
    filename = 'data/WAtimes/data.txt'
    with open(filename, 'a') as file_object:
        file_object.write(html)


# 写入新链接
def save_new_links_to_file():
    with open('data/WAtimes/links.txt', 'a') as file_object:
        for link in news_links:
            file_object.write(link + '\n')


initiate_old_links()
get_news_links('/news/world/')
# 空串
# /specials/coronavirus-covid-19-pandemic-updates/
# /news/world/
get_news(news_links)
save_new_links_to_file()
