
from typing import Any, Dict
import uuid

import pydantic
from utils import aws_parse
from service.crud import model
from service.crud import repository

class Settings(pydantic.BaseSettings):
    restaurant_table_name: str


SETTINGS = Settings()
RESTAURANT_REPOSITORY = repository.RestaurantRepo(SETTINGS.restaurant_table_name)


@aws_parse.parse_lambda_event
def handler(event: aws_parse.LambdaEvent, context: Any) -> Any:
    try:
        result = get_public(**event.params)
        response = aws_parse.get_response(aws_parse.HttpCodes.SUCCESS, result)
    except Exception as e:
        print("Error registering user %s" % (e))
        response = aws_parse.get_response(aws_parse.HttpCodes.ERROR, {"message": str(e)})
    
    return response


def get_public(*args, **kwargs) -> Dict:
    private_restaurants = RESTAURANT_REPOSITORY.scan_public_restaurants(**kwargs) or []
    return {"restaurants": [restaurant.dict() for restaurant in private_restaurants]}