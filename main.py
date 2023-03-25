import requests
from bs4 import BeautifulSoup as BS


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

    return urls


def filter_urls(url_list, filter_text):
    filters_urls = []

    for i in url_list:
        r = requests.get(i)
        html = BS(r.content, 'html.parser')
        page = html.select(
            '.section-main-content > .container-fluid > .postcard-single > .row > .col-xs-12 > .entry-title')
        name = page[0].contents[0]

        if filter_text.lower() in name.lower():
            filters_urls.append(i)

    return filters_urls


raw_urls = parse_urls_by_year(1899, 1899)
filtered_urls = filter_urls(raw_urls, 'Санкт-Петербург')
print(filtered_urls)