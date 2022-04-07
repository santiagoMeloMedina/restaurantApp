from typing import Any, Dict

import pydantic
from utils import aws_parse, validation, encryption
from service.registration import model
from service.registration import repository


class Settings(pydantic.BaseSettings):
    users_table_name: str


SETTINGS = Settings()
USERS_REPOSITORY = repository.RegistrationRepo(SETTINGS.users_table_name)


@aws_parse.parse_lambda_event
def handler(event: aws_parse.LambdaEvent, context: Any) -> Any:
    try:
        if event.body.get("email", None) and event.body.get("password", None):
            result = login_user(**event.body)
            response = aws_parse.get_response(aws_parse.HttpCodes.SUCCESS, result)
        else:
            response = aws_parse.get_response(
                aws_parse.HttpCodes.BAD_REQUEST,
                {"message": "Missing required parameters"},
            )
    except Exception as e:
        print("Error registering user %s" % (e))
        response = aws_parse.get_response(
            aws_parse.HttpCodes.ERROR, {"message": str(e)}
        )

    return response


def _parse_user(email: str, password: str, **kwargs) -> model.User:
    if validation.is_email_valid(email):
        if validation.is_password_valid(password):
            return model.User(email=email, password=password)
        else:
            raise Exception("Not valid password")
    else:
        raise Exception("Not valid email")


def login_user(*args, **kwargs) -> Dict:
    user = _parse_user(**kwargs)
    existing_user = USERS_REPOSITORY.get_user_by_email(user.email)
    if existing_user:
        if (
            user.password
            == encryption.PasswordHandler(existing_user.get("password")).decrypt()
        ):
            return {
                "accessToken": encryption.JWTHandler(
                    payload={"user": user.email}
                ).generate()
            }
        else:
            raise Exception("Incorrect password")
    else:
        raise Exception("User not found")
