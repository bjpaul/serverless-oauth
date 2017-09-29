import traceback

import requests

from common.config import Config

common = Config()
from common.logs import Log
log = Log()

EMP_TTN_EMAIL_KEY = "employee_ttn_email_id"

def validate_ttn_oauth_token(token):
    try:
        response = requests.get(common.ttn_oauth_url + "?access_token=" + str(token),
                                headers={'Content-type': 'application/json'})
        response = response.json()
        return_dict = {}
        return_dict[common.emp_code_key] = response["employeeCode"]
        return_dict[EMP_TTN_EMAIL_KEY] = response["email"]
        return return_dict

    except Exception as e:
        log.debug("Invalid ttn access_token : " + token)
        log.debug(e)
        traceback.print_exc()
        raise Exception(common.un_authorize)


def validate(ttn_oauth_access_token):
    EMP_CODE_KEY = common.emp_code_key

    return_dict = validate_ttn_oauth_token(ttn_oauth_access_token)


    return_dict[common.emp_email_key] = return_dict[EMP_TTN_EMAIL_KEY]
    del return_dict[EMP_TTN_EMAIL_KEY]
    emp_data = {}
    emp_data[EMP_CODE_KEY] = return_dict[EMP_CODE_KEY]
    del return_dict[EMP_CODE_KEY]

    return_dict[common.emp_data_key] = emp_data
    return return_dict
