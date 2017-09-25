import json

from auth.common.config import Config

common = Config()
from auth.token_id import crypto


def id_string_builder(client_request_data):
    data = {"client_secret": common.client_secret}
    data["todo"] = client_request_data["todo"]
    return crypto.encrypt(data)


def validate(jti, client_request_data):
    data = json.loads(crypto.decrypt(jti))
    if data["client_secret"] != common.client_secret:
        return False

    if data["todo"] != client_request_data["todo"]:
        return False

    return True
