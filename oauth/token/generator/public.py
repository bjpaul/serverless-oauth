import traceback

import jwt

from common.config import Config

common = Config()
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from common import log

EMP_EMAIL_KEY = common.emp_email_key

RSA_PRIVATE_KEY = common.id_token_private_key

private_key = serialization.load_pem_private_key(
    RSA_PRIVATE_KEY,
    password=None,
    backend=default_backend())


# Assymmetric encrypted generator: Generating id generator
def generateIdToken(authResponseData, scope, return_dict, error_dict):
    try:
        EMP_DATA_KEY = common.emp_data_key
        EMP_ROLE_KEY = common.emp_roll_key
        EMP_SCOPE_KEY = common.emp_scope_key
        data = {}
        data["token_use"] = "id"
        data[EMP_EMAIL_KEY] = authResponseData[EMP_EMAIL_KEY]
        data[EMP_DATA_KEY] = authResponseData[EMP_DATA_KEY]
        data[EMP_DATA_KEY][common.emp_competency_key] = "[ List of competencies]"
        data[EMP_ROLE_KEY] = authResponseData[EMP_ROLE_KEY]
        data[EMP_SCOPE_KEY] = scope
        token = jwt.encode(data, key=private_key, algorithm=common.ae_algorithm)
        return_dict["id_token"] = token

    except Exception as e:
        log.error(e)
        traceback.print_exc()
        error_dict["id_token_error"] = True
