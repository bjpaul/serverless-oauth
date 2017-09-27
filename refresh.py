import json
from oauth.auth import authenticator


def refresh_handler(event, context):
    refreshToken = event["refresh_token"]
    client_id = event["client_id"]
    client_request_data = json.dumps(event["ttn_oauth_access_token"])
    return authenticator.refresh(refresh_token=refreshToken, client_id=client_id,
                                 client_request_data=client_request_data)
