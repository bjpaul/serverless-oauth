import datetime
import traceback
import jwt
from common.config import Config
from common import crypto
from common import log
from oauth.token import client_request
common = Config()

private_key = common.access_token_secret


class AccessTokenGenerator(object):

    def __init__(self, auth_response_data, scope, audience_id, iat_utc_datetime, client_request_data, token_use, return_dict, error_dict):
        self._auth_response_data = auth_response_data
        self._scope = scope
        self._audience_id = audience_id
        self._iat_utc_datetime = iat_utc_datetime
        self._client_request_data = client_request.build_data(client_request_data)
        self._token_use = token_use
        self._return_dict = return_dict
        self._error_dict = error_dict

    @property
    def auth_response_data(self):
        return self._auth_response_data

    @property
    def scope(self):
        return self._scope

    @property
    def audience_id(self):
        return self._audience_id

    @property
    def iat_utc_datetime(self):
        return self._iat_utc_datetime

    @property
    def token_use(self):
        return self._token_use

    @property
    def client_request_data(self):
        return self._client_request_data

    @property
    def return_dict(self):
        return self._return_dict

    @property
    def error_dict(self):
        return self._error_dict

    # Assymmetric encrypted generator: Encrypting and Generating generator
    def generateToken(self, data):
        return jwt.encode(data, key=private_key, algorithm=common.ae_algorithm)

    def token_id_builder(self, client_request_data):
        return crypto.encrypt(client_request_data)

    # Assymmetric encrypted generator: Generating access generator
    def generate(self):
        EMP_DATA_KEY = common.emp_data_key
        EMP_EMAIL_KEY = common.emp_email_key
        EMP_ROLE_KEY = common.emp_roll_key
        EMP_SCOPE_KEY = common.emp_scope_key
        try:
            token_id = self.token_id_builder(client_request_data=self.client_request_data)
            data = {}
            data["token_use"] = self._token_use
            data["iss"] = common.token_issuer
            data["aud"] = self.audience_id
            data[EMP_EMAIL_KEY] = self.auth_response_data[EMP_EMAIL_KEY]
            # data[EMP_DATA_KEY] = self.auth_response_data[EMP_DATA_KEY]
            data[EMP_ROLE_KEY] = self.auth_response_data[EMP_ROLE_KEY]
            data[EMP_SCOPE_KEY] = self.scope
            data["iat"] = self.iat_utc_datetime

            delta = common.access_token_ttl_sec
            if self._token_use == "refresh":
                delta = common.refresh_token_ttl_sec

            exp_utc_access = self.iat_utc_datetime + datetime.timedelta(seconds=delta)
            data["exp"] = exp_utc_access
            data["jti"] = token_id
            token = self.generateToken(data)
            self.return_dict[self._token_use + "_token"] = token

        except Exception as e:
            log.error(e)
            traceback.print_exc()
            self.error_dict[self._token_use + "_token_error"] = True







