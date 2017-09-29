from common.logs import Log
from oauth.auth import authenticator
from util import response
from common.config import Config
log = Log()
cnf = Config()

def refresh_handler(event, context):
    refreshToken = event["body"]["refresh_token"]
    client_id = event["headers"]["client_id"]
    client_request_data = event["client_request_data"]
    return response.build(authenticator.refresh(refresh_token=refreshToken, client_id=client_id,
                                                client_request_data=client_request_data))


if __name__== "__main__":
    event = {
        "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIxMjM0NSIsImlzcyI6ImFiYy5jb20iLCJ0b2tlbl91c2UiOiJyZWZyZXNoIiwianRpIjoic2FqOUlybGpvcjF6ayIsImV4cCI6MTUwOTEzMTUwOCwiaWF0IjoxNTA2NTM5NTA4LCJzY29wZSI6eyJhY2Nlc3MiOnsiL2dyYW50IjpbIlBPU1QiXSwiL2V2ZW50IjpbIlBBVENIIiwiR0VUIl19LCJncmFudF9hY2Nlc3MiOlsidXBkYXRlLWV2ZW50IiwiZ3JhbnQtYWNjZXNzIiwiZ2V0LWV2ZW50Il19LCJyb2xsIjpbIkFETUlOIl0sInN1YiI6ImJpam95LnBhdWxAdG90aGVuZXcuY29tIn0.gupFbJtlWd50xu8aVm7rgrjeXMWH2Zz7LnIFxaJGiVU",
        "client_id": cnf.client_id,
        "client_request_data": {
            "todo":"TODO"
        }
    }
    log.info(refresh_handler(event, None))