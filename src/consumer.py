
import json
import pymongo

from kafka import KafkaConsumer
from pymongo import MongoClient

consumer = KafkaConsumer('stack',
                         # auto_offset_reset='earliest', # this will start
                         # from the latest entry from the producer
                         enable_auto_commit=True,
                         bootstrap_servers=['localhost:9092'], 
                         api_version=(0, 10),
                         value_deserializer=lambda x: json.loads(x.decode(
                             'utf-8'))
                         )
client = MongoClient('mongodb://localhost:27017')


def save_in_db(question, questions_collection):
    # sample transformation part in ETL process
    question['title'] = question['title'].lower()

    # loading to mongodb part in the ETL process
    questions_collection.insert_one(question)


def get_stack_questions(questions_collection):
    # receiving value sent by the producer
    for message in consumer:
        save_in_db(message.value, questions_collection)


if __name__ == '__main__':
    db_name = client['stackdb']
    questions_collection = db_name['questions']

    get_stack_questions(questions_collection)

    consumer.close()
