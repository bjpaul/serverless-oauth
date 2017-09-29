import datetime
from multiprocessing import Process, Manager
from common.config import Config
from oauth.auth.scope import scope
from oauth.auth import competency
from oauth.auth import user_credentials_validator
from oauth.token.generator.public import IdTokenGenerator
from oauth.token.generator.private import AccessTokenGenerator
from oauth.token.validator import private as TokenValidator
from common.logs import Log
log = Log()
common = Config()
scp = scope.provider()

def add_roles(data):
    emp_email = data[common.emp_email_key]
    data[common.emp_role_key] = scp.list_emp_roles(emp_email)


def grant_scope(data):
    emp_email = data[common.emp_email_key]
    role_list = data[common.emp_role_key]
    return scp.list_emp_scope(emp_email, role_list)


# Asymmetric encrypted generator: validating user credential and generate generator with RSA public key in PEM or SSH format
def login(google_id_token, ttn_oauth_access_token, client_id, client_request_data):
    
    if client_id != common.client_id:
        log.debug("Invalid client id : " + client_id)
        raise Exception(common.un_authorize)
    
    data = user_credentials_validator.validate(google_id_token, ttn_oauth_access_token)

    add_roles(data)

    scope_dict = grant_scope(data)

    iat_utc_datetime = datetime.datetime.utcnow()
    manager = Manager()
    return_dict = manager.dict()

    error_dict = manager.dict()
    error_dict["id_token_error"] = False
    error_dict["access_token_error"] = False
    error_dict["refresh_token_error"] = False
    
    idTokenGenerator = IdTokenGenerator(
        auth_response_data=data,
        scope=scope_dict["id_token_scope_list"],
        return_dict= return_dict,
        error_dict = error_dict
    )
    id_token_process = Process(target=idTokenGenerator.generate)
    
    accessTokenGenerator = AccessTokenGenerator(
        auth_response_data=data, 
        scope=scope_dict["access_token_scope"],
        audience_id=common.client_id,
        iat_utc_datetime=iat_utc_datetime,
        client_request_data=client_request_data,
        return_dict=return_dict,
        error_dict=error_dict,
        token_use="access"
    )
    
    access_token_process = Process(target=accessTokenGenerator.generate)

    refreshTokenGenerator = AccessTokenGenerator(
        auth_response_data=data,
        scope=scope_dict["access_token_scope"],
        audience_id=common.client_id,
        iat_utc_datetime=iat_utc_datetime,
        client_request_data=client_request_data,
        return_dict=return_dict,
        error_dict=error_dict,
        token_use="refresh"
    )
    
    refresh_token_process = Process(target=refreshTokenGenerator.generate)
    id_token_process.start()
    access_token_process.start()
    refresh_token_process.start()

    id_token_process.join()
    access_token_process.join()
    refresh_token_process.join()

    if error_dict["id_token_error"] or error_dict["access_token_error"] or error_dict["refresh_token_error"]:
        raise Exception(common.internal_server_error)

    response = return_dict.copy()  # Making a simple dictionary

    response["access_token_expires_in"] = common.access_token_ttl_sec
    response["refresh_token_expires_in"] = common.refresh_token_ttl_sec
    response["principal"] = data[common.emp_email_key]
    response["token_type"] = "Bearer"
    config = {}
    config["competencies"] = competency.list_competency_config()
    response["config"] = config
    return response


def refresh(refresh_token, client_id, client_request_data):
    data = TokenValidator.validate(refresh_token, client_id, client_request_data)
    iat_utc_datetime = datetime.datetime.utcnow()
    response = {}
    error = {"access_token": False}
    
    accessTokenGenerator = AccessTokenGenerator(
        auth_response_data=data,
        scope=data[common.emp_scope_key],
        audience_id=client_id,
        iat_utc_datetime=iat_utc_datetime,
        client_request_data=client_request_data,
        return_dict=response,
        error_dict=error,
        token_use="access"
    )
    
    accessTokenGenerator.generate()

    if error["access_token"]:
        raise Exception(common.internal_server_error)

    response["access_token_expires_in"] = common.access_token_ttl_sec
    response["token_type"] = "Bearer"
    return response