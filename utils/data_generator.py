from faker import Faker

fake = Faker()


def full_name() -> str:
    return fake.name()


def email() -> str:
    return fake.email()


def address() -> str:
    return fake.address().replace("\n", " ")
