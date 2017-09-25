import datetime
from multiprocessing import Process, Manager

from auth.common.config import Config

common = Config()
from auth.login import user_credentials_validator, scope
from auth.token_generator import public, private


def generate_config(config):
    config[common.emp_scope_key] = scope.all_scope_list()


def add_roles(data):
    emp_email = data[common.emp_email_key]
    data[common.emp_roll_key] = scope.list_emp_roles(emp_email)


def grant_scope(data, all_scopes):
    emp_email = data[common.emp_email_key]
    role_list = data[common.emp_roll_key]
    return scope.list_emp_scope(emp_email, role_list, all_scopes)


# Asymmetric encrypted token_generator: validating user credential and generate token_generator with RSA public key in PEM or SSH format
def validate(google_id_token, ttn_oauth_access_token, client_request_data):
    data = user_credentials_validator.validate(google_id_token, ttn_oauth_access_token)
    config = {}

    generate_config(config)
    add_roles(data)

    scope_dict = grant_scope(data, config[common.emp_scope_key])

    iat_utc_datetime = datetime.datetime.utcnow()
    manager = Manager()
    return_dict = manager.dict()

    error_dict = manager.dict()
    error_dict["id_token_error"] = False
    error_dict["access_token_error"] = False
    error_dict["refresh_token_error"] = False

    id_token_process = Process(target=public.generateIdToken,
                               args=(data, scope_dict["id_token_scope_list"], return_dict, error_dict))

    access_token_process = Process(target=private.generate_token,
                                   args=(data, scope_dict["access_token_scope"], common.client_id, iat_utc_datetime, client_request_data, "access",
                                         return_dict, error_dict))
    refresh_token_process = Process(target=private.generate_token,
                                    args=(data, scope_dict["access_token_scope"], common.client_id, iat_utc_datetime, client_request_data, "refresh",
                                          return_dict, error_dict))
    id_token_process.start()
    access_token_process.start()
    refresh_token_process.start()

    id_token_process.join()
    access_token_process.join()
    refresh_token_process.join()

    if error_dict["id_token_error"] or error_dict["access_token_error"] or error_dict["refresh_token_error"]:
        raise Exception('Internal server error')

    response = return_dict.copy()  # Making a simple dictionary

    response["access_token_expires_in"] = common.access_token_ttl_sec
    response["refresh_token_expires_in"] = common.refresh_token_ttl_sec
    response["principal"] = data[common.emp_email_key]
    response["token_type"] = "Bearer"
    response["app_name"] = common.app_name
    response["request_id"] = common.request_id
    response["config"] = config
    return response
