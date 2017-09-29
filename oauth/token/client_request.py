from common.config import Config
from common.logs import Log
import json
cnf = Config()
log = Log()


def build_data(meta_data):
    client_request_data = json.dumps(meta_data)
    log.debug("Incoming client request meta data : "+client_request_data)
    log.debug("collect_client_request_metadata : "+str(cnf.collect_client_request_metadata))

    if cnf.collect_client_request_metadata:
        data = json.loads(client_request_data)
        data["client_secret"] = cnf.client_secret
    else:
        data = {"client_secret": cnf.client_secret}
    logData = data
    logData["client_secret"] = "*****"
    log.debug("Transformed client request meta data : " + str(logData))
    return data
