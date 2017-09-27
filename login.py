from oauth.auth import authenticator
import json

def login_handler(event, context):
    idToken = event["google_id_token"]
    ttnOauthAccessToken = event["ttn_oauth_access_token"]

    client_request_data = json.dumps(event["ttn_oauth_access_token"])
    return authenticator.login(google_id_token=idToken, ttn_oauth_access_token=ttnOauthAccessToken,
                                   client_request_data=client_request_data)
