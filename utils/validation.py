import re

EMAIL_REGEX_EXPRESSION = (
    "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)
PASSWORD_REQUIRED_FIELDS = "!@#?]"


def is_email_valid(email: str) -> str:
    validation = re.compile(EMAIL_REGEX_EXPRESSION)
    return bool(re.fullmatch(validation, email))


def is_password_valid(password: str) -> str:
    password_conditions = lambda x: [
        len(x) >= 10,
        any([sub_x.islower() for sub_x in x]),
        any([sub_x.isupper() for sub_x in x]),
        all([(req in password) for req in PASSWORD_REQUIRED_FIELDS]),
    ]
    return all(password_conditions({letter for letter in password}))


# print(is_password_valid("]2@#Aa!8?0"))
