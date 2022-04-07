

import rsa
from configuration import aws_keys

class PasswordHandler:
    def __init__(self, pub_path: str, password: str) -> None:
        self.param_handler = aws_keys.ParamsHandler()
        self.password = password
        self.pub_path = pub_path

    def encrypt(self):
        return rsa.encrypt(self.password, self.param_handler.get_secure_param(self.pub_path))
    
    def decrypt(self):
        return rsa.decrypt(self.password, )