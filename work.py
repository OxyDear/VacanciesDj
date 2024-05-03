import requests
import codecs
from bs4 import BeautifulSoup as bs

errors = []
domain = 'https://www.work.ua'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'
jobs = []


def getContent():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    response = requests.get(url=url, headers=headers)

    with codecs.open('content.html', 'w', 'utf-8') as file:
        if response.status_code == 200:
            file.write(str(response.text))
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    file.close()


try:
    with open('content.html', 'r') as file:
        resp = file.read()
except FileNotFoundError:
    getContent()

# if resp == '':
#     getContent()

if resp != '':
    soup = bs(resp, 'html.parser')
    main_div = soup.find('div', id='pjax-jobs-list')
    if main_div:
        div_list = main_div.find_all('div', attrs={'class': 'job-link'})
        for div in div_list:
            title = div.find('h2').a.text
            href = div.find('h2').a['href']
            content = div.p.text
            company = 'No name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({'title': title, 'url': domain + href, 'content': content, 'company': company})
    else:
        errors.append({'url': url, 'title': 'Div does not exist'})

with codecs.open('work.json', 'w', 'utf-8') as file:
    file.write(str(jobs))
file.close()
