import traceback
import json

from common import config

from oauth.auth import authenticator
from util.response import Builder


def login_handler(event, context):
    client_request_data = config.init(event)
    try:
        body = json.loads(event["body"])
        headers = event["headers"]
        ttnOauthAccessToken = body["ttn_oauth_access_token"]
        client_id = headers["client_id"]
    except Exception as e:
        traceback.print_exc()
        return Builder.bad_request_error_message(e.message)
    
    builder = Builder(target=authenticator.login, args=(ttnOauthAccessToken,client_id, client_request_data))
    return builder.build()


if __name__== "__main__":
    headers = {"client_id":"12345"}
    body = "{\n    \"google_id_token\":\"eyJhbGciOiJSUzI1NiIsImtpZCI6IjhlYzE3OTk0Mzk0NDY0ZDk1YjBiM2Q5MDYzMjZmMWNkZGU4YWVlNjQifQ.eyJhenAiOiI0MTU5ODM0NjU0OTUtZzU1aGdpOW82ajBwYzhwZTJlMmFwMGZjdmoxbHBvaG4uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MTU5ODM0NjU0OTUtZzU1aGdpOW82ajBwYzhwZTJlMmFwMGZjdmoxbHBvaG4uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDU3NTcwNzQxNTQ3NzYxOTQ2NTAiLCJoZCI6InRvdGhlbmV3LmNvbSIsImVtYWlsIjoiYmlqb3kucGF1bEB0b3RoZW5ldy5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Il84N2JDdTMzMmJCV0hCdENxUU5xT1EiLCJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwianRpIjoiZDk5NzJlM2MzZTE3OGIyMzk3MGFjZmFmZGVlN2E1NGE0NjI1MDM2ZiIsImlhdCI6MTUwNjY2OTM1NSwiZXhwIjoxNTA2NjcyOTU1LCJuYW1lIjoiQmlqb3kgUGF1bCIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLWYwS3Q3TTNzQldjL0FBQUFBQUFBQUFJL0FBQUFBQUFBQlpvL3N5NGEtdzZlYko4L3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJCaWpveSIsImZhbWlseV9uYW1lIjoiUGF1bCIsImxvY2FsZSI6ImVuIn0.k-_S5jBq5bB0jjQbhv5Ss-7RUsZVKn3Q2Q5Pn-2PIB_PAqBWuZXtEAh_myBU1XfzCtYa5QqW0kKguzIABjn91Q8pkvj3-eR46PnaDEpQGgQtutvyPpJX4hs27jzOqZmceaALnj3MngXwrKUzAkMl51hMOlhr6QRxODDH-CcHfHTsUNHhX2m6CDf8DbWrgmsrKLMs_izfam68Se7_XNccRosgqV5krIg_rwRs0lJlLWF2EFF1sc9SvqkOKmsDT7GlTgVK5j6tJVINL07WP2GHzdn3XPKdL-c69RCJCGWc2aNS0OyICjLq3Q_f__EixQ4vUVcOJKm6sR312dXVV0kd7w\"," "\n    \"ttn_oauth_access_token\":\"2d3418bf-9699-4ad1-9ec9-b2e1555facd9\"\n}"
    event = {"resource":"/login","path":"/login","httpMethod":"POST","headers":headers,"queryStringParameters":None,"pathParameters":None,"stageVariables":None,"requestContext":{"path":"/login","accountId":"187632318301","resourceId":"gzmhx0","stage":"test-invoke-stage","requestId":"test-invoke-request","identity":{"cognitoIdentityPoolId":None,"accountId":"187632318301","cognitoIdentityId":None,"caller":"AIDAJHP6ODTX6ZTLMAC3I","apiKey":"test-invoke-api-key","sourceIp":"test-invoke-source-ip","accessKey":"ASIAJPA6PQYVRHSTL7EA","cognitoAuthenticationType":None,"cognitoAuthenticationProvider":None,"userArn":"arn:aws:iam::187632318301:user/geekcombat","userAgent":"Apache-HttpClient/4.5.x (Java/1.8.0_131)","user":"AIDAJHP6ODTX6ZTLMAC3I"},"resourcePath":"/login","httpMethod":"POST","apiId":"dhxwub3cn5"},"body":body,"isBase64Encoded":False}
    print(json.dumps(login_handler(event ,None)))

