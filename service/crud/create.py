
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
        result = create_restaurant(**event.body)
        response = aws_parse.get_response(aws_parse.HttpCodes.SUCCESS, result)
    except Exception as e:
        print("Error registering user %s" % (e))
        response = aws_parse.get_response(aws_parse.HttpCodes.ERROR, {"message": str(e)})
    
    return response


def create_restaurant(*args, **kwargs) -> Dict:
    restaurant_data = {
        "owner": kwargs.get("user"), 
        "id": str(uuid.uuid4()), 
        **kwargs
    }
    restaurant = model.Restaurant.parse_obj(restaurant_data)
    RESTAURANT_REPOSITORY.put_restaurant(restaurant)
    return restaurant.dict()