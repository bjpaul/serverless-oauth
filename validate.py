from oauth.token.validator import private
import json


def validation_handler(event, context):
    client_request_data = json.dumps(event["ttn_oauth_access_token"])
    client_id = event["client_id"]
    accessToken = event["refresh_token"]
    return private.validate(accessToken, client_id=client_id, client_request_data=client_request_data)
