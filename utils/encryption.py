

import base64
import pydantic
import binascii
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
        self.__encryption_key: str = secret_key.get('Parameter', {}).get('Value', None)
        if not self.__encryption_key:
            raise Exception("No secret key provided")

    def encrypt(self):
        fernet = Fernet(base64.urlsafe_b64encode(binascii.unhexlify(self.__encryption_key)))
        return fernet.encrypt(self.password.encode())
    
    def decrypt(self):
        fernet = Fernet(base64.urlsafe_b64encode(binascii.unhexlify(self.__encryption_key)))
        return fernet.decrypt(self.password).decode()