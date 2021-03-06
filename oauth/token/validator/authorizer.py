from __future__ import print_function
import traceback
from oauth.token.validator.policy import AuthPolicy
from oauth.token.validator.policy import HttpVerb
from oauth.token.validator import private
from common import config
from common.logs import Log
from util.response import Builder
import json

log = Log()

def validate(event):
    return authorize(event)
    
def authorize(event):
    # log.debug("********** jwt payload > "+str(event))
    client_request_data = config.init(event)
    try:
        body = json.loads(event["body"])
        accessToken = body['authorizationToken']
        headers = event["headers"]
        client_id = headers["client_id"]
    except Exception as e:
        traceback.print_exc()
        return Builder.bad_request_error_message(e.message)

    payload = private.validate(accessToken, client_id, client_request_data)
    # client_request_data = config.init(event)
    # client_id = event["client_id"]
    # accessToken = event['authorizationToken']

    '''
    Validate the incoming token and produce the principal user identifier
    associated with the token. This can be accomplished in a number of ways:

    1. Call out to the OAuth provider
    2. Decode a JWT token inline
    3. Lookup in a self-managed DB
    '''
    # payload = private.validate(accessToken, client_id=client_id, client_request_data=client_request_data)
    log.debug("********** jwt payload > "+str(payload))
    principalId = payload["sub"]

    '''
    You can send a 401 Unauthorized response to the client by failing like so:

      raise Exception('Unauthorized')

    If the token is valid, a policy must be generated which will allow or deny
    access to the client. If access is denied, the client will receive a 403
    Access Denied response. If access is allowed, API Gateway will proceed with
    the backend integration configured on the method that was called.

    This function must generate a policy that is associated with the recognized
    principal user identifier. Depending on your use case, you might store
    policies in a DB, or generate them on the fly.

    Keep in mind, the policy is cached for 5 minutes by default (TTL is
    configurable in the authorizer) and will apply to subsequent calls to any
    method/resource in the RestApi made with the same token.

    The example policy below denies access to all resources in the RestApi.
    '''
    method_arn = "arn:aws:execute-api:us-east-1:187632318301:dhxwub3cn5/*/POST/login"
    # method_arn = event['methodArn']
    tmp = method_arn.split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]

    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]

    data = payload["scope"]["access"]
    for endpoint, httpMethods in data.iteritems():
        for httpMethod in httpMethods:
            policy.allowMethod(httpMethod["http_method"], endpoint)

    # Finally, build the policy
    authResponse = policy.build()

    # new! -- add additional key-value pairs associated with the authenticated principal
    # these are made available by APIGW like so: $context.authorizer.<key>
    # additional context is cached
    context = json.dumps(payload)

    authResponse['context'] = context

    return authResponse
