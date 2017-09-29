import traceback
from oauth.token.validator import authorizer
from common.config import Config
from common.logs import Log
log = Log()
cnf = Config()

def validation_handler(event, context):

    def success_message_builder(data):
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

    def error_message_builder(errorMessage):
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

    try:
        return success_message_builder(authorizer.authorize(event))
    except Exception as e:
        traceback.print_exc()
        return error_message_builder(e.message)


if __name__== "__main__":
    headers = {"client_id": "12345"}
    body = "{\n    \"authorizationToken\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.9JSbvNmL3VmblhGdvRHQsVXYw5SevpWaiJiOiIWdzJCL91VfiM3clN2Yh1CduFmcnJiOiUWbh52Xu9Wa0NWYisHL9JCduVmdl1SZ0FGZwVnI6ISZtFmbf52bpR3YhJCLdJSYk5WZnFWL05WZ2VWLlRXYkBXdiwiI5NmblRXZw12bj1CduVmdl1SZ0FGZwVnIsIibvlGdhN2bs1CduVmdl1SZ0FGZwVnIsICdvx2ctQnblZXZtUGdhRGc1JyW6IyczV2YjF2XlNmc192clJ3X05WZ2VmI7xSfiQnblZXZtQXZnJiOiUWbh52Xu9Wa0NWYis3W6IyczV2YjF2X05WYydmIs0XX91lIhRmbldWYtQnblZXZtUGdhRGc1JCLik3YuVGdlBXbvNWL05WZ2VWLlRXYkBXdiwiIu9Wa0F2YvxWL05WZ2VWLlRXYkBXdiwiI09Gbz1CduVmdl1SZ0FGZwVnIbpjIzNXZjNWYfV2YyV3bzVmcfRnblZXZiwiIINEVBBlI6ICZvhGdl12XwRHdoJyes0nIUV0RiojIk9Ga0VWbfBHd0hmI7tlOiQnblZXZvICLd1nIUN1TQJiOiQ2boRXZt9Fc0RHais3W6ICduFmcn9iI7pjIzNXZjNWYisnOiUGcvN2ciwSOwADM3YjNwUTM6ICdhlmIskDM2MzN2YDM1EjOiAHelJCLdJiTJ1ERBJyW6ISZs9mciwiIzNXZjNWYiojIlNXdf5WZr9GdiwiIt92YuMmYhJiOiM3cpJCLiUDNzITMiojIkVXYiwiIVhkaUVDcQNjLaBVYzJiOikGdqJye.aYv4Fsv4qSUqOmSdD8SS_1awbdVf4cXm92G2n6uCeR8\"}"
    event = {"resource": "/validate", "path": "/validate", "httpMethod": "POST", "headers": headers,
             "queryStringParameters": None, "pathParameters": None, "stageVariables": None,
             "requestContext": {"path": "/login", "accountId": "187632318301", "resourceId": "gzmhx0",
                                "stage": "test-invoke-stage", "requestId": "test-invoke-request",
                                "identity": {"cognitoIdentityPoolId": None, "accountId": "187632318301",
                                             "cognitoIdentityId": None, "caller": "AIDAJHP6ODTX6ZTLMAC3I",
                                             "apiKey": "test-invoke-api-key", "sourceIp": "test-invoke-source-ip",
                                             "accessKey": "ASIAJPA6PQYVRHSTL7EA", "cognitoAuthenticationType": None,
                                             "cognitoAuthenticationProvider": None,
                                             "userArn": "arn:aws:iam::187632318301:user/geekcombat",
                                             "userAgent": "Apache-HttpClient/4.5.x (Java/1.8.0_131)",
                                             "user": "AIDAJHP6ODTX6ZTLMAC3I"}, "resourcePath": "/login",
                                "httpMethod": "POST", "apiId": "dhxwub3cn5"}, "body": body, "isBase64Encoded": False}
    log.info(validation_handler(event, None))
