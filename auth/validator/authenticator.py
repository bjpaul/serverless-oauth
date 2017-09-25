from auth.token_id import jti
from auth.validator import private_token_validator


def validate(e_token, client_id, client_request_data):
    payload = private_token_validator.validate_ae_token(e_token=e_token, audience_id=client_id)

    if jti.validate(jti=payload["jti"], client_request_data=client_request_data):
        return payload
    else:
        raise Exception('Unauthorized')
