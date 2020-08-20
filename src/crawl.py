
import json
import requests

from bs4 import BeautifulSoup
from kafka import KafkaProducer

base_url = 'https://stackoverflow.com'

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             api_version=(0, 10),
                             value_serializer=lambda v: json.dumps(v).encode(
                                 'utf-8'))


def get_all_questions(soup):
    questions = list()

    selector = 'div.summary > h3 > a'
    all_question_links = soup.select(selector)

    for question in all_question_links:
        question = f"{base_url}{question['href']}"
        questions.append(question)
        
    return questions


def get_question_details(question):
    question_details = dict()

    details = requests.get(question)

    details_soup = BeautifulSoup(details.content, 'html.parser')

    title = details_soup.find(id='question-header').find(
        'h1').find('a').text
    tags_element = details_soup.find('div', 'grid ps-relative '
                                           'd-block').find_all('a')
    tags = [elem.text for elem in tags_element]

    question_details['title'] = title
    question_details['tags'] = tags
    question_details['url'] = question

    # sending to consumer
    producer.send('stack', value=question_details)

    return question_details


def main():
    # tags = ['python', 'django', 'aws', 'json']
    tags = ['javascript', 'php', 'html', 'jquery', 'mysql']
    for tag in tags:
        for i in range(1, 20):
            url = f'https://stackoverflow.com/questions/tagged/' \
                  f'{tag}?tab=newest&page={i}&pagesize=50'
            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            # get all questions
            all_questions = get_all_questions(soup)

            # get question details, performing the extract part of ETL
            for question in all_questions:
                get_question_details(question)


if __name__ == '__main__':
    main()

    producer.flush()
