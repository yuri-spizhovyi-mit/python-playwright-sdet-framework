# Faker, random data
from faker import Faker

fake = Faker()


def email():
    return fake.email()
