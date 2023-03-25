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

    for i in url_list:
        r = requests.get(i)
        html = BS(r.content, 'html.parser')
        page = html.select(
            '.section-main-content > .container-fluid > .postcard-single > .row > .col-xs-12 > .entry-title')
        name = page[0].contents[0]

        if filter_text.lower() in name.lower():
            filters_urls.append(i)

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

raw_urls = parse_urls_by_year(1891, 2014)
# filtered_urls = filter_urls(raw_urls, 'Санкт-Петербург')
# print(filtered_urls)
word_list = get_keywords(raw_urls)

word_dict = {}
for word in word_list:
    if word in word_dict:
        word_dict[word] += 1
    else:
        word_dict[word] = 1

word_dict = dict(sorted(word_dict.items(), key=lambda x: x[1], reverse=True))

file = open('words.txt', 'w')

word_dict_size = len(word_dict)
cur = 0

for i in word_dict.keys():
    file.write(str(word_dict[i]) + ' ' + str(i) + '\n')
    os.system('clear')
    print(f'Done {cur /  word_dict_size * 100}%')

os.system('clear')
print('Done!')


file.write('<endoftext>')
file.close()
