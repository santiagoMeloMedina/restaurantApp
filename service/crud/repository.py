from typing import Any, Dict, List, Optional
import boto3
from boto3.dynamodb import conditions
from service.crud import model


class RestaurantRepo:
    def __init__(self, table_name: str):
        dynamodb_resource = boto3.resource("dynamodb")
        self.table = dynamodb_resource.Table(table_name)

    def get_restaurant_by_id(self, id: str) -> Optional[model.Restaurant]:
        response = self.table.get_item(Key={"id": id})
        return (
            model.Restaurant.parse_obj(response.get("Item"))
            if "Item" in response
            else None
        )

    def scan_restaurants_by_user(self, email: str) -> List[model.Restaurant]:
        response = self.table.scan(FilterExpression=conditions.Attr("owner").eq(email))
        return [model.Restaurant.parse_obj(item) for item in response.get("Items")]

    def scan_public_restaurants(
        self, limit: int, offset: int
    ) -> List[model.Restaurant]:
        response = self.table.scan(FilterExpression=conditions.Attr("public").eq(True))
        return [model.Restaurant.parse_obj(item) for item in response.get("Items")][
            limit:offset
        ]

    def put_restaurant(self, restaurant: model.Restaurant) -> Any:
        response = self.table.put_item(Item=restaurant.dict())
        return response
