
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
        result = get_by_id(**event.body)
        response = aws_parse.get_response(aws_parse.HttpCodes.SUCCESS, result)
    except Exception as e:
        print("Error registering user %s" % (e))
        response = aws_parse.get_response(aws_parse.HttpCodes.ERROR, {"message": str(e)})
    
    return response


def get_by_id(*args, **kwargs) -> Dict:
    if "id" in kwargs:
        restaurant = RESTAURANT_REPOSITORY.get_restaurant_by_id(kwargs.get("id"))
        if kwargs.get("user", "") == restaurant.owner:
            return restaurant.dict()
        else:
            raise Exception(f"Only the owner can see this restaurant {kwargs.get('id')}")
    else:
        raise Exception("No ID specified to get restaurant")