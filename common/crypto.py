import json
import crypt

from common.config import Config

common = Config()
key = common.encryption_salt


def encrypt(data):
    return crypt.crypt(json.dumps(data), key)


def validate(data, encrypted_data):
    return crypt.crypt(json.dumps(data), key) == encrypted_data

