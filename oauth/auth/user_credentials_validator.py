import traceback
from multiprocessing import Process, Manager

import requests

from common.config import Config

common = Config()
from oauth2client import client, crypt
from common import log

EMP_TTN_EMAIL_KEY = "employee_ttn_email_id"
GOOGLE_TTN_EMAIL_KEY = "employee_google_email_id"

def validate_google_id_token(token, client_id, return_dict, error_dict):
    try:
        # idinfo = client.verify_id_token(generator, None)
        idinfo = client.verify_id_token(token, client_id)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer -> " + idinfo['iss'])

        if not idinfo['email_verified']:
            raise crypt.AppIdentityError("Unverified email")

        if idinfo['hd'] != common.hosted_domain:
            raise crypt.AppIdentityError("Wrong host domain -> " + idinfo['hd'])
        return_dict[GOOGLE_TTN_EMAIL_KEY] = idinfo["email"]
        return_dict[common.emp_name_key] = idinfo["name"]
        return_dict[common.emp_image_key] = idinfo["picture"]
        return_dict[common.google_user_id_key] = idinfo['sub']

    except Exception as e:
        log.debug("Invalid google id_token : " + token)
        log.debug(e)
        traceback.print_exc()
        error_dict["google_error"] = True


def validate_ttn_oauth_token(token, return_dict, error_dict):
    try:
        response = requests.get(common.ttn_oauth_url + "?access_token=" + str(token),
                                headers={'Content-type': 'application/json'})
        response = response.json()
        return_dict[common.emp_code_key] = response["employeeCode"]
        return_dict[EMP_TTN_EMAIL_KEY] = response["email"]

    except Exception as e:
        log.debug("Invalid ttn access_token : " + token)
        log.debug(e)
        traceback.print_exc()
        error_dict["ttn_error"] = True


def validate(google_id_token, ttn_oauth_access_token):
    EMP_NAME_KEY = common.emp_name_key
    EMP_IMAGE_KEY = common.emp_image_key
    EMP_CODE_KEY = common.emp_code_key
    GOOGLE_USER_ID_KEY = common.google_user_id_key

    manager = Manager()
    return_dict = manager.dict()
    error_dict = manager.dict()
    error_dict["google_error"] = False
    error_dict["ttn_error"] = False

    p1 = Process(target=validate_google_id_token,
                 args=(google_id_token, common.google_client_id, return_dict, error_dict))
    p1.start()
    p2 = Process(target=validate_ttn_oauth_token, args=(ttn_oauth_access_token, return_dict, error_dict))
    p2.start()
    p1.join()
    p2.join()

    if error_dict["google_error"] or error_dict["ttn_error"]:
        raise Exception('Unauthorized')

    if return_dict[GOOGLE_TTN_EMAIL_KEY] != return_dict[EMP_TTN_EMAIL_KEY]:
        log.debug("Error: Google email id : " + str(return_dict[GOOGLE_TTN_EMAIL_KEY]) + " != ttn email id : " + str(
            return_dict[EMP_TTN_EMAIL_KEY]))
        raise Exception('Unauthorized')

    return_dict[common.emp_email_key] = return_dict[GOOGLE_TTN_EMAIL_KEY]
    del return_dict[GOOGLE_TTN_EMAIL_KEY]
    del return_dict[EMP_TTN_EMAIL_KEY]
    emp_data = {}
    emp_data[EMP_CODE_KEY] = return_dict[EMP_CODE_KEY]
    emp_data[GOOGLE_USER_ID_KEY] = return_dict[GOOGLE_USER_ID_KEY]
    emp_data[EMP_NAME_KEY] = return_dict[EMP_NAME_KEY]
    emp_data[EMP_IMAGE_KEY] = return_dict[EMP_IMAGE_KEY]
    del return_dict[EMP_CODE_KEY]
    del return_dict[GOOGLE_USER_ID_KEY]

    return_dict[common.emp_data_key] = emp_data
    return return_dict
