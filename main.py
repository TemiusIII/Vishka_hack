# -*- coding: utf-8 -*-

import os

import openai
import requests
from bs4 import BeautifulSoup as BS

# from kandinsky2 import get_kandinsky2

openai.organization = "org-8KTKwP5PvIxmALryYT18cgPQ"
openai.api_key = "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"

# model = get_kandinsky2('cuda', task_type='text2img')


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

    file = open('white_list.txt', 'r')
    filter_keywords = file.read().split('\n')

    for keyword in keywords:
        if keyword not in final_keywords and keyword in filter_keywords:
            final_keywords.append(keyword)

    return final_keywords


def generate_prompts(keywords, start, end, area):
    system_passage = '''
    ты -  эксперт в истории, ты знаешь важные события которые произошли в эпохи:
    1. 1891-1916
    2. 1917-1940
    3. 1941-1965
    4. 1966-1985
    5. 1986-1992
    6. 1993-2014

    События, котрые ты знаешь:

    1)1891-1916
    начало масштабного (1891—1892) голода в России.
    Александр III подписал именной высочайший указ, данный министру путей сообщений, о строительстве Транссибирской железной дороги.
    в Петербурге в ночь с 20 декабря арестованы В. И. Ленин и другие руководители Союза борьбы за освобождение рабочего класса.
    «Кровавое воскресенье», начало Первой русской революции
    начало всеобщей политической стачки в России, бастуют даже Госбанк и министерства

    2)1917-1940
    Переход от капитализма к социализму связанный с принятием конституции РСФСР 1925 года это отображало изменение в государственном строительстве, окончание гражданской войны, восстановление народного хозяйства
    3) Программой празднования запланировано более 230 общегородских
    праздничных мероприятий. Мероприятия приуроченные к 67 годовщине Победы в
    Великой Отечественной Войне 1941-1945 годов
    4)1966-1985 период застоя/Эпоха застоя
    Развитие страны в 1964-1986 продолжилось. Однако зависимость от экспорта полезных ископаемых привела к отсутствию необходимых реформ в экономики. Это повлияло на отставание в высокотехнологических областях, низкое качество продукции, неэффективное производство и низкий уровень производственного труда.
    5)1986-1992
    В 1988 предприятие воспользовалось законом «О государственном предприятии (объединение)» которое было принято 30 июня 1987 года. Для повышение зарплат, рост цен, а так же дефицит в торговле. В это время начал процветать «черный» рынок. Прямые связи между предприятиями выродились в бартерный обмен, т.к. на рубли нельзя было ничего купить.
    В 1990 вышел первый номер газеты «Коммерсант». Основатель и главный редактор газеты, журналист Яковлев, который ориентировался на «Нью-Йорк таймс». «Коммерсант» сразу создавался как бизнес-проект, получавший доход от рекламы.
    В 1892 произошла либерализация цен это позволяло полагаться на восстановление рублёвых расчётов. Для того чтобы облегчить наполнение рынка товарами была либерализована и внешняя торговля.
    6)1993-2014
    1993г
    На территории России вступил закон о въезде и выезде, который прияла советская власть в 1991, но он так и не был реализован
    Военный парад в Москве в честь 50-й годовщины победы над фашистской Германией.
    Начало трехдневной общероссийской забастовки работников просвещения, в которой участвовали 300 тыс. человек. В феврале прошли массовые забастовки шахтеров (500 тыс. участников). Бастующие требовали ликвидировать огромную задолженность по зарплате.
    2007г
    «Рособоронэкспорт» стал единственным в России экспортером вооружений и техники. На создание второй после «Газпрома» экспортной монополии возлагались надежды исключить «ненужную конкуренцию между российскими производителями военной техники на внешнем рынке». Отныне все новые соглашения производители вправе заключать только через «Рособоронэкспорт». В обход госпосредника им разрешено продавать за рубеж лишь запчасти и обслуживать ранее проданную технику. Монополист стал торговать умело, что с сожалением признавали его конкуренты на мировых рынках. Экспорт российского оружия неуклонно нарастал.
    25 мая
    Северная Корея в ответ на международное давление в связи с её ядерной программой демонстративно провела испытание ядерного оружия. Уже 4 апреля 2009 года Корея запустила многоступенчатую ракету, показывая, что может использовать её в военных целях. В ответ совет ООН ужесточил санкции и разрешил досматривать суда и самолёты с грузами. Пхеньян ( столица и крупнейший город КНДР) расценил это как «объявление войны» и отказался от шести сторонних переговоров по ядерной проблеме. Но к концу года многосторонний диалог всё же возобновился.
    2014. 22 зимние Олимпийские игры в Сочи. Россия заняла первое место с 13 золотыми 11 серебряными и 9 бронзовыми медалями. Во время церемонии Олимпийских игр одно и колец не раскрылось. Нераскрывшееся кольцо стало неофициальным символом российских игр. К Олимпиаде было построено 6 спортивных сооружений в Олимпийском парке и 5 – в горном кластере.
    '''

    prompt = f'''
    Напиши несколько разных идеальных prompts для генерации картинок для midjourney, которые описывают {start}-{end} в локации {area}, опираясь на свои знания. Обязательно используй слова из жтого списка в prompt:{', '.join(keywords)} Если список пуст, то просто опирайся на свои зания. Добавь \"<endofpassage>\" в конце каждого prompt.
    Выведи список в формате
    1. ...
    2. ...
    3. ...
    '''

    # Generate a response using the GPT-3 API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_passage},
            {"role": "user", "content": prompt},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    result = result.split('<endofpassage>')
    for i in range(len(result)):
        for j in '1. |2. |3. |4. |5. |6. '.split('|'):
            result[i] = result[i].replace(j, '')
    result.pop()

    return result



# def create_and_save(prompts):
#     cnt = 1
#
#     os.makedirs('/kaggle/working/result', exist_ok=True)
#     for prompt in prompts:
#         images = model.generate_text2img(prompt, batch_size=2, h=512, w=512, num_steps=75,
#                                          denoised_type='dynamic_threshold', dynamic_threshold_v=99.5,
#                                          sampler='ddim_sampler', ddim_eta=0.05, guidance_scale=10)
#         for i in range(len(images)):
#             images[i].save(f'/kaggle/working/result/{cnt}.png')
#             cnt += 1


def fast_keywords(start, end):
    input_file = open("fast_keywords.txt", "r", encoding="utf-8")
    dicta = {}

    for t_line in input_file:
        line = t_line[0:-1]
        date, lst = line.split(None, 1)
        lst = lst.strip("[]").replace("'", "").split(",")
        dicta[date] = lst

    keywords = []
    for i in range(start, end + 1):
        for word in dicta[str(i)]:
            if word != '' and word not in keywords:
                keywords.append(word)

    return keywords


def pipeline(start, end, area):
    # raw_urls = parse_urls_by_year(start, end)
    # filtered_urls = filter_urls(raw_urls, area)
    # raw_keywords = get_keywords(filtered_urls)
    # final_keywords = filter_keywords(raw_keywords)
    final_keywords = fast_keywords(start, end)
    print(final_keywords)
    prompts = generate_prompts(final_keywords, start, end, area)
    print(prompts)

    # create_and_save(prompts)


# pipeline(1941, 1945, 'Москва')
