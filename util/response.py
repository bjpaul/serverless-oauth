import traceback
from common.config import Config

cnf = Config()


class Builder(object):
    def __init__(self, target=None, args=()):
        self._target = target
        self._args = tuple(args)

    def build(self):
        try:
            return self.success_message_builder(self._target(*self._args))
        except Exception as e:
            traceback.print_exc()
            return self.error_message_builder(e.message)

    def success_message_builder(self, data):
        statusCode = 200
        successMessage = {
            "code": statusCode,
            "data": data,
            "app_name": cnf.app_name,
            "request_id": cnf.request_id
        }
        return {"statusCode":statusCode, "body": str(successMessage)}

    @staticmethod
    def bad_request_error_message(message):
        statusCode = 400
        errorObject = {
            "code": statusCode,
            "error_type": "BadRequest",
            "app_name": cnf.app_name,
            "request_id": cnf.request_id,
            "message": message
        }
        return {"statusCode": statusCode, "body": str(errorObject)}

    def error_message_builder(self, errorMessage):
        if errorMessage == cnf.un_authorize:
            statusCode = 401
            errorObject = {
                "code": statusCode,
                "error_type": "Unauthorized",
                "app_name": cnf.app_name,
                "request_id": cnf.request_id,
                "message": errorMessage
            }

        elif errorMessage == cnf.forbidden:
            statusCode = 403
            errorObject = {
                "code": statusCode,
                "error_type": "Forbidden",
                "app_name": cnf.app_name,
                "request_id": cnf.request_id,
                "message": errorMessage
            }
        else:
            statusCode = 500
            errorObject = {
                "code" : statusCode,
                "error_type": "InternalServerError",
                "app_name": cnf.app_name,
                "request_id": cnf.request_id,
                "message": "An unknown error has occurred. Please try again."
            }
        return {"statusCode": statusCode, "body": str(errorObject)}
