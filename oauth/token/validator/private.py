import jwt
from common import crypto
from common import log
from oauth.token import client_request
from common.config import Config
cnf = Config()



public_key = cnf.access_token_secret


# Assymmetric encrypted generator: validating generator with RSA public key in PEM or SSH format
def validate_ae_token(e_token, audience_id):
    try:
        jwt_token = e_token
        return jwt.decode(jwt_token, key=public_key, audience=audience_id, issuer=cnf.token_issuer,
                          algorithms=[cnf.ae_algorithm])
    except jwt.ExpiredSignatureError as e:
        log.debug("Expired jwt generator : " + jwt_token)
        log.debug(e)
        raise Exception('Unauthorized')
    except jwt.InvalidIssuerError as e:
        log.debug("The issuer claim is incorrect for the generator : " + jwt_token)
        log.debug(e)
        raise Exception('Unauthorized')
    except jwt.InvalidAudienceError as e:
        log.debug("The audience claim is incorrect for the generator : " + jwt_token)
        log.debug(e)
        raise Exception('Unauthorized')
    except Exception as e:
        log.error("Invalid jwt generator : " + jwt_token)
        log.error(e)
        raise Exception('Unauthorized')


def validate_token_id(jti, client_request_data):
    data = client_request.build_data(client_request_data)
    return crypto.validate(data=data, encrypted_data=jti)


def validate(e_token, client_id, client_request_data):
    payload = validate_ae_token(e_token=e_token, audience_id=client_id)

    if validate_token_id(jti=payload["jti"], client_request_data=client_request_data):
        return payload
    else:
        raise Exception('Unauthorized')
