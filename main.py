import requests
from bs4 import BeautifulSoup as BS
import os


def parse_urls_by_year(start, end):
    urls = []
    pg = 1
    for i in range(start, end + 1):
        r = requests.get(f'https://sysblok.ru/postcards/postcard-year/{i}')
        html = BS(r.content, 'html.parser')

        pages = html.select(
            '.postcards__page > .postcards__container > .postcard__item > .post-card > .entry-thumb-link')

        for page in pages:
            urls.append(page['href'])
        os.system('clear')
        print("Parsed year", i)

    print("Done!")
    return urls


def filter_urls(url_list, filter_text):
    filters_urls = []
    urls_size = len(url_list)
    cur = 0

    for i in url_list:
        r = requests.get(i)
        html = BS(r.content, 'html.parser')
        page = html.select(
            '.section-main-content > .container-fluid > .postcard-single > .row > .col-xs-12 > .entry-title')
        name = page[0].contents[0]

        if filter_text.lower() in name.lower():
            filters_urls.append(i)

        os.system('clear')
        print(f'Done {cur / urls_size * 100}%')
        cur += 1

    return filters_urls


def get_keywords(urls):
    keywords = []
    urls_size = len(urls)
    cur = 0

    for url in urls:
        r = requests.get(url)
        html = BS(r.content, 'html.parser')
        pages = html.select(
            '.section-main-content > .container-fluid > .postcard-single > .row > .col-xs-12 > .postcard-tags > .postcard-tag')

        for page in pages:
            keywords.append(str(page.contents[0]))

        os.system('clear')
        print(f'Done {cur / urls_size * 100}%')
        cur += 1

    print("Done!")
    return keywords


def filter_keywords(keywords):
    filter_keywords = []
    final_keywords = []
    keywords_size = len(keywords)
    cur = 0

    file = open('white_list.txt', 'r')
    temp = file.readline()
    while temp != '<endoftext>':
        filter_keywords.append(temp)
        temp = file.readline()

    for keyword in keywords:
        if keyword not in final_keywords and keyword in filter_keywords:
            final_keywords.append(keyword)
        os.system('clear')
        print(f'Done {cur / keywords_size * 100}%')
        cur += 1

    return final_keywords


first, last = 1891, 1916
area = ''
urls = parse_urls_by_year(first, last)
filtered_urls = filter_urls(urls, area)
raw_keywords = get_keywords(filtered_urls)
print(raw_keywords)
final_keywords = filter_keywords(raw_keywords)
print(final_keywords)