from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from first_job.models import Vacancy
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup


# save data to db
def save_new_vacancy(title, city, salary, description, employer, link, source, publication_date):
    object = Vacancy.objects.create(
        title=title,
        city=city,
        salary=salary,
        description=description,
        employer=employer,
        job_link=link,
        source=source,
        publication_date=publication_date
    )
    object.save()


# prepare publication date for saving to db
def get_publication_date(date):
    month_dict = {'января': 1, 'січеня': 1, 'лютого': 2, 'березенья': 3, 'квітеня': 4, 'травня': 5,
                  'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'червня': 6, 'липня': 7, 'июля': 7}
    day = date[0]
    month = month_dict[date[1]]
    year = date[2]
    return datetime.strptime(f'{day}.{month}.{year}', "%d.%m.%Y")


@shared_task
def pars_dou_job():
    # get all job_links from db
    all_vacancy_job_link = [x.job_link for x in Vacancy.objects.all().only('job_link')]

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome('/home/alexandr/PycharmProjects/first_job_for_junior/scraping/dou_job_ua/chromedriver',
                              chrome_options=options)
    driver.get("https://jobs.dou.ua/vacancies/?search=Python&exp=1-3")
    sleep(2)

    try:
        driver.find_element(By.XPATH,
                            '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/a').click()
    except Exception:
        pass
    sleep(2)

    # get all cards
    cards = driver.find_elements(By.CLASS_NAME, 'vt')
    links = []

    for card in cards:
        links.append(card.get_attribute('href'))

    for link in links:

        # if link absent in all_vacancy_job_link get vacancy
        if link not in all_vacancy_job_link:

            sleep(2)
            driver.get(link)

            description = driver.find_element(By.XPATH,
                                              '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[4]').text

            title = driver.find_element(By.XPATH,
                                        '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/h1').text
            city = driver.find_element(By.XPATH,
                                       '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/span').text
            employer = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/a[1]').text

            publication_date_clean = driver.find_element(By.XPATH,
                                                         '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[3]'
                                                         ).text.split(' ')[:3]

            try:
                salary = driver.find_element(By.XPATH,
                                             '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/div[1]/span[2]'
                                             ).text
            except Exception:
                salary = 'Зароботная плата не указана'

            date_to_db = get_publication_date(publication_date_clean)
            source = 'jobs.dou.ua'

            save_new_vacancy(title, city, salary, description, employer, link, source, date_to_db)

    driver.close()
    driver.quit()


@shared_task
def pars_rabota_ua():
    from requests_html import HTMLSession
    all_vacancy_job_link = [x.job_link for x in Vacancy.objects.all().only('job_link')]
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome('/home/alexandr/PycharmProjects/first_job_for_junior/scraping/rabota_ua/chromedriver',
                              chrome_options=options)
    driver.get("https://rabota.ua/zapros/junior-python-developer")
    sleep(2)

    # get all cards
    cards = driver.find_elements(By.TAG_NAME, 'a')

    links = []
    for card in cards:
        vacansy_namber = card.get_attribute('href').split('/')[-1]  # get card number
        word = "".join(" " if el.isdigit() else el for el in vacansy_namber).split()  # check card number
        if "".join(word) == 'vacancy':
            links.append(card.get_attribute('href'))  # add card link to list

    for link in links:
        if link not in all_vacancy_job_link:
            driver.get(link)  # get card
            sleep(2)

            description = driver.find_element(By.ID, 'description-wrap').text  # get job_description
            city = driver.find_element(By.XPATH,
                                       '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div/div/lib-content/div[2]/div[4]/span[1]').text  # noqa
            try:
                title = driver.find_element(By.XPATH,
                                            '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div/div/lib-content/div[1]/div[1]/h1').text  # noqa
            except Exception:
                title = driver.find_element(By.XPATH,
                                            '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div/div/lib-content/div[1]/div[1]/h1').text  # noqa
            try:
                salary = driver.find_element(By.XPATH,
                                             '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div/div/lib-content/div[1]/div[1]/div[4]/span[1]').text  # noqa
            except Exception:
                salary = 'Зароботная плата не указана'
            try:
                employer = driver.find_element(By.XPATH,
                                               '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div[2]/div/div[2]/lib-content/div[2]/div[2]/a/span').text  # noqa
            except Exception:
                employer = driver.find_element(By.XPATH,
                                               '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div/div/lib-content/div[1]/div[1]/h1').text  # noqa
            try:
                session = HTMLSession()
                get_code = session.get(link)
                get_code.html.render(timeout=30)
                try:
                    publication_date_clean = get_code.html.xpath(
                        '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div'
                        '/div/lib-content/div[2]/santa-tooltip/div/div[2]/div/span').text

                except IndexError:
                    publication_date_clean = get_code.html.xpath(
                        '/html/body/app-root/div[1]/alliance-jobseeker-vacancy-page/article/div[1]/div/div/div/'
                        'lib-content/div[2]/santa-tooltip/div/div[2]/div/span')[0].text.split(' ')
                try:
                    date_to_db = get_publication_date(publication_date_clean)
                except TypeError:
                    date_to_db = datetime.now()
            except AttributeError:
                date_to_db = datetime.now()

            # if description not in all_vacancy_description:  # filtered vacancy by description,
            source = 'rabota.ua'  # if vacancy not exist save vacancy to db
            save_new_vacancy(title, city, salary, description, employer, link, source, date_to_db)

    driver.close()
    driver.quit()


@shared_task
def pars_work_ua():
    all_vacancy_job_link = [x.job_link for x in Vacancy.objects.all().only('job_link')]
    clean_link = []
    page = 1

    # get all links
    while True:
        heders = Headers().generate()

        url = 'https://www.work.ua/ru/jobs-pyrhon/'
        params = {
            'page': page,
        }
        res = requests.get(url, headers=heders, params=params)

        page += 1
        soup = BeautifulSoup(res.text, 'html.parser')

        description_job = soup.findAll('h2', {'class': ''})
        if description_job == []:
            break

        stat_path = 'https://www.work.ua'
        for job in description_job:
            try:
                # titles = job.find('a').get('title')
                # for title in titles.split(' '):
                #     if title in ('Junior', 'Middle'):
                link = job.find('a').get('href')
                path = stat_path + link
                clean_link.append(path)
            except AttributeError:
                pass

    for link in clean_link:
        if link not in all_vacancy_job_link:
            res = requests.get(link, headers=heders)

            soup = BeautifulSoup(res.text, 'html.parser')
            description_job = soup.findAll('div', {'class': 'card wordwrap'})

            for job in description_job:
                description = job.find('div', {'id': 'job-description'}).text

                title = job.find('h1', {'id': 'h1-name'}).text

                # TODO
                try:
                    employer = job.find('span', {
                        'class': 'glyphicon glyphicon-company text-black glyphicon-large'
                    }).find('a', 'title').text
                    print(employer, ' a')
                except AttributeError:
                    employer = job.find('p', {
                        'class': 'text-indent text-muted add-top-sm'
                    }).findNext('b').text
                    print(employer, ' b')

                city = list(job.find('p', {'class': 'text-indent add-top-sm'}).text.replace('\n', '').strip().split(','))[0]

                try:
                    salary = job.find('b', {'class': 'text-black'}).text
                except AttributeError:
                    salary = 'Зарплата не указана '

                try:
                    publication_date = job.find('span', {'class': 'text-muted'}).text
                    # publication_date = ' '.join(publication_date.replace('\xa0', ' ').split(' ')[2:])
                    publication_date_clean = publication_date.replace('\xa0', ' ').split(' ')[2:]
                    date_to_db = get_publication_date(publication_date_clean)
                except AttributeError:
                    date_to_db = datetime.now()


                source = 'work.ua'  # if vacancy not exist save vacancy to db
                save_new_vacancy(title, city, salary, description, employer, link, source, date_to_db)


@shared_task
def contact_us_mail(email_to):
    from django.core.mail import send_mail
    from django.conf import settings
    subject = 'Contact us email',
    full_email_massage = '''
           Hello!

           We receive your question and soon answer you!
           '''

    send_mail(
        subject,
        full_email_massage,
        settings.EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )
