import datetime
import traceback

import jwt

from common.config import Config

common = Config()
from common import crypto
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from common import log

RSA_PRIVATE_KEY = common.access_token_private_key

private_key = serialization.load_pem_private_key(
    RSA_PRIVATE_KEY,
    password=common.pem_passphrase,
    backend=default_backend())


# Assymmetric encrypted generator: Encrypting and Generating generator
def generateToken(data):
    return jwt.encode(data, key=private_key, algorithm=common.ae_algorithm)


# Assymmetric encrypted generator: Generating access generator
def generate_token(auth_response_data, scope, audience_id, iat_utc_datetime, client_request_data, token_use, return_dict, error_dict):
    EMP_DATA_KEY = common.emp_data_key
    EMP_EMAIL_KEY = common.emp_email_key
    EMP_ROLE_KEY = common.emp_roll_key
    EMP_SCOPE_KEY = common.emp_scope_key
    try:
        token_id = token_id_builder(client_request_data=client_request_data)
        data = {}
        data["token_use"] = token_use
        data["iss"] = common.token_issuer
        data["aud"] = audience_id
        data[EMP_EMAIL_KEY] = auth_response_data[EMP_EMAIL_KEY]
        # data[EMP_DATA_KEY] = auth_response_data[EMP_DATA_KEY]
        data[EMP_ROLE_KEY] = auth_response_data[EMP_ROLE_KEY]
        data[EMP_SCOPE_KEY] = scope
        data["iat"] = iat_utc_datetime

        delta = common.access_token_ttl_sec
        if token_use == "refresh":
            delta = common.refresh_token_ttl_sec

        exp_utc_access = iat_utc_datetime + datetime.timedelta(seconds=delta)
        data["exp"] = exp_utc_access
        data["jti"] = token_id
        token = generateToken(data)
        return_dict[token_use+"_token"] = token

    except Exception as e:
        log.error(e)
        traceback.print_exc()
        error_dict[token_use+"_token_error"] = True


def token_id_builder(client_request_data):
    data = {"client_secret": common.client_secret}
    data["todo"] = client_request_data["todo"]
    return crypto.encrypt(data)