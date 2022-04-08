import os
import binascii

print(f"Your password key: {binascii.hexlify(os.urandom(32)).decode()}")
