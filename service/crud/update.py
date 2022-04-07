from typing import Any, Dict

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
        result = update_restaurant(**event.body)
        response = aws_parse.get_response(aws_parse.HttpCodes.SUCCESS, result)
    except Exception as e:
        print("Error registering user %s" % (e))
        response = aws_parse.get_response(
            aws_parse.HttpCodes.ERROR, {"message": str(e)}
        )

    return response


def update_restaurant(*args, **kwargs) -> Dict:
    if "id" in kwargs:
        restaurant = RESTAURANT_REPOSITORY.get_restaurant_by_id(kwargs.get("id"))
        if kwargs.get("user", "") == restaurant.owner:
            del kwargs["id"]
            if "owner" in kwargs:
                del kwargs["owner"]
            restaurant_data = {**restaurant.dict(), **kwargs}
            restaurant = model.Restaurant.parse_obj(restaurant_data)
            RESTAURANT_REPOSITORY.put_restaurant(restaurant)
            return restaurant.dict()
        else:
            raise Exception(f"Only the owner can update restaurant {kwargs.get('id')}")
    else:
        raise Exception("No ID specified to update restaurant")
