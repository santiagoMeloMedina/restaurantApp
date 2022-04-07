

import base64
import datetime
import pydantic
import binascii
import jwt
from cryptography.fernet import Fernet
from configuration import aws_keys

class PasswordHandler:

    class Settings(pydantic.BaseSettings):
        password_secure_path: str
        
    def __init__(self, password: str) -> None:
        self.password = password
        self.settings = self.Settings()
        self.__set_params()
    
    def __set_params(self):
        secret_key = aws_keys.ParamsHandler().get_secure_param(self.settings.password_secure_path)
        self.__encryption_key: str = secret_key
        if not self.__encryption_key:
            raise Exception("No secret key provided")

    def encrypt(self):
        fernet = Fernet(base64.urlsafe_b64encode(binascii.unhexlify(self.__encryption_key)))
        return fernet.encrypt(self.password.encode())
    
    def decrypt(self):
        fernet = Fernet(base64.urlsafe_b64encode(binascii.unhexlify(self.__encryption_key)))
        return fernet.decrypt(self.password.encode()).decode()


class JWTHandler:

    ALGORITHM = "HS256"

    class Settings(pydantic.BaseSettings):
        token_secret_key: str
        
    def __init__(self, payload: str = None, token: str = None) -> None:
        self.payload = payload
        self.token = token
        self.settings = self.Settings()
        self.__set_params()
    
    def __set_params(self):
        secret_key = aws_keys.ParamsHandler().get_secure_param(self.settings.token_secret_key)
        self.__secret_key: str = secret_key
        if not self.__secret_key:
            raise Exception("No secret key provided")
        
    def generate(self):
        self.payload["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1)
        return jwt.encode(self.payload, self.__secret_key, algorithm=self.ALGORITHM)
    
    def decoce(self):
        return jwt.decode(self.token, self.__secret_key, algorithms=self.ALGORITHM)