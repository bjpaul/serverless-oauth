import datetime

from auth.common.config import Config

common = Config()
from auth.token_generator import private
from auth.validator import authenticator


def token(refresh_token, client_id, client_request_data):
    data = authenticator.validate(refresh_token, client_id, client_request_data)
    iat_utc_datetime = datetime.datetime.utcnow()

    response = {}
    error = {"access_token":False}
    private.generate_token(auth_response_data=data, scope= data[common.emp_scope_key], audience_id=client_id, iat_utc_datetime=iat_utc_datetime, client_request_data=client_request_data, token_use="access", return_dict=response, error_dict=error)

    if error["access_token"]:
        raise Exception("Interbal server error")

    response["access_token_expires_in"] = common.access_token_ttl_sec
    response["token_type"] = "Bearer"
    response["app_name"] = common.app_name
    response["request_id"] = common.request_id

    return response


