from common.config import Config
import json
cnf = Config()


def build_data(client_request_data):
    data = json.loads(client_request_data)
    return {
        "todo": data["todo"],
        "client_secret": cnf.client_secret
    }
