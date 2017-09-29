import json
import crypt

from common.config import Config

common = Config()
key = common.encryption_salt


def encrypt(data):
    if common.enable_jti_encryption:
        return crypt.crypt(json.dumps(data), key)
    else:
        return data


def validate(data, encrypted_data):
    if common.enable_jti_encryption:
        return crypt.crypt(json.dumps(data), key) == encrypted_data
    else:
        return True


def reverse_token(token):
    token_split = token.split(".")
    header = token_split[0]
    payload = token_split[1]
    signature = token_split[2]
    return header + "." + payload[::-1] + "." + signature
