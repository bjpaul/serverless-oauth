import json

from cryptography.fernet import Fernet

from common.config import Config

common = Config()
# key = Fernet.generate_key()
key = common.encryption_key
cipher_suite = Fernet(key)


def encrypt(data):
    return cipher_suite.encrypt(json.dumps(data))


def decrypt(data):
    return cipher_suite.decrypt(json.dumps(data))
