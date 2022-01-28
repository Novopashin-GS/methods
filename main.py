import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://spb.hh.ru/search/vacancy'
params = {'text': input('Введите интересующую вас вакансию: '),
          'page': 0}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
job_list = []
while True:
    response = requests.get(url, params=params, headers=headers).text
    dom = BeautifulSoup(response, 'html.parser')
    job_data = dom.find_all('div', attrs={'class': 'vacancy-serp-item'})
    for job in job_data:
        job_param = {'name': job.find('a', attrs={'class': 'bloko-link'}).getText(),
                     'link': job.find('a', attrs={'class': 'bloko-link'}).get('href'),
                     'site': 'hh.ru'
                     }
        try:
            salary = (job.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()).replace(
                '\u202f', '')
        except:
            salary = None
        if salary:
            if 'от' in salary:
                min_salary = float(salary.split('т ')[1].split('0 ')[0] + '0')
                max_salary = None
                currency = salary.split('0 ')[1]
            elif 'до' in salary:
                max_salary = float(salary.split('о ')[1].split('0 ')[0] + '0')
                min_salary = None
                currency = salary.split('0 ')[1]
            else:
                min_salary = float(salary.split(' –')[0])
                max_salary = float(salary.split('– ')[1].split(' ')[0])
                currency = salary.split('– ')[1].split(' ')[1]
        else:
            min_salary = None
            max_salary = None
            currency = None
        job_param['min_salary'] = min_salary
        job_param['max_salary'] = max_salary
        job_param['currency'] = currency
        job_list.append(job_param)
    if dom.find('a', {'data-qa': 'pager-next'}):
        params['page'] += 1
    else:
        break
pprint(job_list)

