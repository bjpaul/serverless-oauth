from oauth.auth import authenticator
from common import log
import json


def login_handler(event, context):
    idToken = event["google_id_token"]
    ttnOauthAccessToken = event["ttn_oauth_access_token"]
    client_request_data = json.dumps(event["client_request_data"])
    return authenticator.login(google_id_token=idToken, ttn_oauth_access_token=ttnOauthAccessToken,
                               client_request_data=client_request_data)


if __name__== "__main__":
    event = {
        "google_id_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjViMDkyNGY2ZjgzYzcxOTUxNDk4Nzk1NGNmNjY2ODNiMzcwNjc3ZDQifQ.eyJhenAiOiI0MTU5ODM0NjU0OTUtZzU1aGdpOW82ajBwYzhwZTJlMmFwMGZjdmoxbHBvaG4uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MTU5ODM0NjU0OTUtZzU1aGdpOW82ajBwYzhwZTJlMmFwMGZjdmoxbHBvaG4uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDU3NTcwNzQxNTQ3NzYxOTQ2NTAiLCJoZCI6InRvdGhlbmV3LmNvbSIsImVtYWlsIjoiYmlqb3kucGF1bEB0b3RoZW5ldy5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IkZEeE0yZnlCdTl0NE5YeWFNdE9zcUEiLCJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwianRpIjoiNTg2N2ViMmM3NmY4NjEwMGJiNWNhOGY3NTJlMGM1YWFmMDc2YTgyYyIsImlhdCI6MTUwNjU0MDc5NSwiZXhwIjoxNTA2NTQ0Mzk1LCJuYW1lIjoiQmlqb3kgUGF1bCIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLWYwS3Q3TTNzQldjL0FBQUFBQUFBQUFJL0FBQUFBQUFBQlpvL3N5NGEtdzZlYko4L3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJCaWpveSIsImZhbWlseV9uYW1lIjoiUGF1bCIsImxvY2FsZSI6ImVuIn0.o_d7WJKg118aXsxFNigSms4Z2igGvVdLqjpXnse_TJXV3YsptyByiCjALsibR_9xcOKq6QFxjbagfOnsO_rhzXgazRhR8SHeOk9rHFTXeQEHm52rELx7lRJd5J_ANfjPtHVfDVWoIkKz2o73-Hf6xrYIG3xq1O_F6H7Av2PztEcsD4zyca4Xl_xp_G6HBJqxuRmJu-08Pf4x465mHHknK6AVO21GDdzDmjaT4eoRJKmX7cjz5HhIrLm7aBYsdI9LQVCPutKw21s6A-8GdXOcAevOBSS2abzv4p0_FOD9WPDRFwhFhdcALdil4Jw9pP_nx2UkoLebE-YSpD0GjDsHkg",
        "ttn_oauth_access_token": "2d3418bf-9699-4ad1-9ec9-b2e1555facd9",
        "client_request_data": {
            "todo":"TODO"
        }
    }
    log.info(login_handler(event ,None))
