import jwt

from auth.common.config import Config

common = Config()
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from auth.common import log

# This RSA public key will not be shared with the client, so the access and refresh token_generator can not be decoded at the client side
RSA_PUBLIC_KEY = common.access_token_public_key

public_key = serialization.load_pem_public_key(
    RSA_PUBLIC_KEY,
    backend=default_backend())


# Assymmetric encrypted token_generator: validating token_generator with RSA public key in PEM or SSH format
def validate_ae_token(e_token, audience_id):
    try:
        jwt_token = e_token
        return jwt.decode(jwt_token, key=public_key, audience=audience_id, issuer=common.token_issuer,
                          algorithms=[common.ae_algorithm])
    except jwt.ExpiredSignatureError as e:
        log.debug("Expired jwt token_generator : " + jwt_token)
        log.debug(e)
        raise Exception('Unauthorized')
    except jwt.InvalidIssuerError as e:
        log.debug("The issuer claim is incorrect for the token_generator : " + jwt_token)
        log.debug(e)
        raise Exception('Unauthorized')
    except jwt.InvalidAudienceError as e:
        log.debug("The audience claim is incorrect for the token_generator : " + jwt_token)
        log.debug(e)
        raise Exception('Unauthorized')
    except Exception as e:
        log.error("Invalid jwt token_generator : " + jwt_token)
        log.error(e)
        raise Exception('Unauthorized')
