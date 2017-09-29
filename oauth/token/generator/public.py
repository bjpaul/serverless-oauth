import traceback
import jwt
from common.config import Config
from common.logs import Log
log = Log()

common = Config()
EMP_EMAIL_KEY = common.emp_email_key

private_key = common.id_token_secret


class IdTokenGenerator(object):
    def __init__(self, auth_response_data, scope, return_dict, error_dict):
        self._auth_response_data = auth_response_data
        self._scope = scope
        self._return_dict = return_dict
        self._error_dict = error_dict

    @property
    def auth_response_data(self):
        return self._auth_response_data

    @property
    def scope(self):
        return self._scope

    @property
    def return_dict(self):
        return self._return_dict

    @property
    def error_dict(self):
        return self._error_dict

    # Assymmetric encrypted generator: Generating id generator
    def generate(self):
        try:
            EMP_DATA_KEY = common.emp_data_key
            EMP_ROLE_KEY = common.emp_role_key
            EMP_SCOPE_KEY = common.emp_scope_key
            data = {}
            data["token_use"] = "id"
            authResponseData = self.auth_response_data
            data[EMP_EMAIL_KEY] = authResponseData[EMP_EMAIL_KEY]
            data[EMP_DATA_KEY] = authResponseData[EMP_DATA_KEY]
            data[EMP_DATA_KEY][common.emp_competency_key] = "[ List of competencies]"
            data[EMP_ROLE_KEY] = authResponseData[EMP_ROLE_KEY]
            data[EMP_SCOPE_KEY] = self.scope
            token = jwt.encode(data, key=private_key, algorithm=common.ae_algorithm)
            self.return_dict["id_token"] = token

        except Exception as e:
            log.error(e)
            traceback.print_exc()
            self.error_dict["id_token_error"] = True
