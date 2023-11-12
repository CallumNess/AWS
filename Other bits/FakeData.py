from faker import Faker
import random
import csv
import datetime

fake = Faker()


def capitalize(str):
    return str.capitalize()


def get_rider_name():
    words = fake.words()
    capitalized_words = list(map(capitalize, words))
    return ' '.join(capitalized_words)


def get_brand():
    words = fake.words()
    capitalized_words = list(map(capitalize, words))
    return ' '.join(capitalized_words)


def get_random():
    words = fake.words()
    capitalized_words = list(map(capitalize, words))
    return ' '.join(capitalized_words)


def generate_data():
    return [get_rider_name(), get_brand(), get_random()]


with open('rider_details.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Brand', 'Random'])
    for n in range(1, 100):
        writer.writerow(generate_data())
