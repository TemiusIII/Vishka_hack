import requests
from bs4 import BeautifulSoup as BS

def parse_year(start, end):
    urls = []
    pg = 1
    for i in range(start, end + 1):
        r = requests.get(f'https://sysblok.ru/postcards/postcard-year/{i}')
        html = BS(r.content,  'html.parser')
            
        pages = html.select('.postcards__page > .postcards__container > .postcard__item > .post-card > .entry-thumb-link')
            
        for page in pages:
            urls.append(page['href'])
    
    return urls


print(len(parse_year(1945, 1950)))
print(parse_year(1945, 1950))