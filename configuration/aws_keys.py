
import boto3


class ParamsHandler:
    def __init__(self):
        self.client = boto3.client("ssm")

    def get_secure_param(self, path: str) -> str:
        return self.client.get_parameter(path, WithDecryption=True)
