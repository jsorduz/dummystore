import random
import string


def random_char(length, lowercase: bool = None) -> str:
    valid_chars = string.ascii_letters + string.digits + string.punctuation
    if lowercase is True:
        valid_chars = string.ascii_lowercase
    return "".join(random.choice(valid_chars) for _ in range(length))


def random_email(length=7):
    return f"{random_char(length, lowercase=True)}@example.com"
