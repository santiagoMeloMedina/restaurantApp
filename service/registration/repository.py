
from typing import Dict, Optional
import boto3


class RegistrationRepo:
    def __init__(self, table_name: str):
        dynamodb_resource = boto3.resource("dynamodb")
        self.table = dynamodb_resource.Table(table_name)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        response = self.table.get_item(Key={
            "email": email
        })
        return response.get('Item') if 'Item' in response else None
    
    def put_user(self, email: str, password: str):
        response = self.table.put_item(Item={
            "email": email,
            "password": password
        })
        print(response)
        return response