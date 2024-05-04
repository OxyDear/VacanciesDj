import requests
import codecs
import fake_useragent
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
import time
import json

jobs = []
errors = []
url = 'https://rabota.by/search/vacancy?text=Python&from=suggest_post&area=1002&page='
fk = fake_useragent.UserAgent()

with codecs.open('rabota.html', 'r', 'utf-8') as file:
    src = file.read()

soup = bs(src, 'html.parser')
browser = wd.Safari()


def getContent(url):
    browser.get(url)
    time.sleep(3)

    with codecs.open('rabota.html', 'w', 'utf-8') as file:
        file.write(str(browser.page_source))
    file.close()
    return browser.page_source


# getContent(url+'0')

if src != '':

    pager = soup.find('div', class_='pager')
    for page in range(len([i for i in pager])-1):
        soup = bs(getContent(url + str(page)), 'html.parser')
        print(url+str(page))

        main_div = soup.find('div', id='a11y-main-content')
        if main_div:
            for div in main_div.children:
                if div.name == 'div' and not div.has_attr('class'):
                    title = div.find('h3')
                    urlVac = title.find('a')['href']
                    company = 'No name'
                    if div.find('div', class_='vacancy-serp-item__meta-info-company'):
                        company = div.find('div', class_='vacancy-serp-item__meta-info-company').text
                    resp = requests.get(url=urlVac, headers={'User-Agent': fk.random})
                    soupVac = bs(resp.text, 'html.parser')
                    content = 'Empty'
                    if soupVac.find('div', class_='l-paddings b-vacancy-desc'):
                        content = soupVac.find('div', class_='l-paddings b-vacancy-desc').text
                    elif soupVac.find('div', class_='vacancy-section'):
                        content = soupVac.find('div', class_='vacancy-section').text
                    if title is not None:
                        print(title.text, urlVac, company, content)
                    jobs.append({"title": title.text.replace("'", '').replace('"', ''), "url": urlVac, "content": content.replace("'", '').replace('"', ''), "company": company.replace("'", '').replace('"', '')})
        else:
            errors.append({"url": url, "title": "Div does not exist"})

with codecs.open('jobs.txt', 'w', 'utf-8') as file:
    file.write(str(jobs))

with codecs.open('jobs.txt', 'r', 'utf-8') as file:
    src = file.read().replace(r"'", r'"').replace(r"\xa0", r' ')
    src = json.loads(src)

with codecs.open('jobs.json', 'w', 'utf-8') as file:
    file.write(json.dumps(src, indent=4, ensure_ascii=False))
