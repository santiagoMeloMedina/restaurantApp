import boto3
import os

USERS_DATA = [
    {
        "email": "santiago1@gmail.com",
        "password": "gAAAAABiT55WjkJU9brjMSiVZJlP9w15XDqDXuynFXeTWmT3awkQcaXaeHJMRZY9x54XvkzNxQxrC5KmwaFiDdL2DuKbG5EZsQ==",
    },
    {
        "email": "santiago2@gmail.com",
        "password": "gAAAAABiT56eUJd2VZarlmeYSfFwiFvvT4KWX25ZFtpAL33paHmoBC6xNS6HPktPA0DiH6u10G6C1yaZFzwGgNSK4Hdd--GD8g==",
    },
]

RESTAURANTS_DATA = [
    {
        "category": "Comida Tipica",
        "id": "6482cf46-7bfd-48e2-839e-a15d191a909b",
        "name": "Steaks",
        "owner": "santiago2@gmail.com",
        "public": False,
        "rate": 5,
        "schedule": {"close": "21:00", "days": ["MONDAY", "TUESDAY"], "open": "10:00"},
    },
    {
        "category": "Comida Asiatica",
        "id": "a691f6e0-3d20-41d4-952c-70f25ab95cbc",
        "name": "Heres",
        "owner": "santiago2@gmail.com",
        "public": False,
        "rate": 5,
        "schedule": {"close": "21:00", "days": ["TUESDAY"], "open": "10:00"},
    },
    {
        "category": "Comida Rapida",
        "id": "c97adf27-282b-4061-82c2-4ed6af68cd24",
        "name": "Foods",
        "owner": "santiago1@gmail.com",
        "public": True,
        "rate": 5,
        "schedule": {"close": "21:00", "days": ["FRIDAY"], "open": "15:00"},
    },
]

dynamodb_resource = boto3.resource("dynamodb")
users_table = dynamodb_resource.Table(os.environ.get("USERS_TABLE_NAME"))
for user in USERS_DATA:
    users_table.put_item(Item=user)


dynamodb_resource = boto3.resource("dynamodb")
restaurants_table = dynamodb_resource.Table(os.environ.get("RESTAURANT_TABLE_NAME"))
for restaurant in RESTAURANTS_DATA:
    restaurants_table.put_item(Item=restaurant)
