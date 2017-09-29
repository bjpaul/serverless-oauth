import traceback
import boto3
from botocore.exceptions import ClientError
from common.logs import Log
from common import config
from oauth.auth.scope.base import Base
common = config.Config()
log = Log()

acl_action_order = common.acl_action_order
acl_action_endpoint = common.acl_action_endpoint
acl_action_http_method = common.acl_action_http_method
acl_action_key = common.acl_action_key
event_resources_access_key = common.event_resources_access_key
acl_action_display_key = common.acl_action_display_key
grant_access_key = "grant-access"

if config.env != "dev":
    dynamodb = boto3.resource('dynamodb')
    scope_table = dynamodb.Table('scope')
    employee_role_scope_table = dynamodb.Table('employee_roles')
    role_scopes_table = dynamodb.Table('role_scopes')

class DynamoDB(Base):

    def __init__(self):
        self._emp_email_id = None
        self._emp_roles = None
        self._emp_allowed_event_resource_access = None
        self._emp_blocked_scope = None
        self._emp_blocked_grant_scope = None

    # Resource access
    def all_scope_list(self):
        try:
            response = scope_table.scan()
            scope_list = dict()
            if response.has_key("Items"):
                for item in response["Items"]:
                    scope_list[item[acl_action_key]] = item
            return scope_list
        except ClientError as e:
            traceback.print_exc()
            log.error(e.response['Error']['Message'])
            raise Exception(common.internal_server_error)
    
    # Resource access
    def list_emp_roles(self, emp_email_id):
        self._emp_email_id = emp_email_id
        try:
            key = {'employee_email_id': emp_email_id}
            response = employee_role_scope_table.get_item(Key=key)
            if response.has_key("Item"):
                self._emp_roles = response["Item"][common.emp_role_key].split(",")
                self._emp_blocked_scope = response["Item"]["blocked_scope"].split(",")
                self._emp_blocked_grant_scope = response["Item"]["blocked_grant_scope"].split(",")
            else:
                log.error("No roll found for the user > " + emp_email_id)
                raise Exception(common.forbidden)
        except ClientError as e:
            traceback.print_exc()
            log.error(e.response['Error']['Message'])
            raise Exception(common.internal_server_error)
        return self._emp_roles

    
    # Resource access
    def list_role_scopes(self, role_list):
        # TODO: Query optimization
        # http: // boto3.readthedocs.io / en / latest / reference / services / dynamodb.html  # DynamoDB.Client.batch_get_item
        try:
            acl_action_list = []
            event_resources_access_list = []
            for role in role_list:
                key = {common.emp_role_key: role}
                response = role_scopes_table.get_item(Key=key)
                if response.has_key("Item"):
                    acl_action_list.extend(response["Item"][acl_action_key].split(","))
                    event_resources_access_list.extend(response["Item"][event_resources_access_key].split(","))
                else:
                    log.error("Given role has no scope access > " + role_list)
                    raise Exception(common.forbidden)
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise Exception(common.internal_server_error)

        acl_action_set = set(acl_action_list)
        event_resources_access_set = set(event_resources_access_list)
        scope_list = []
        for acl_action in acl_action_set:
            scope = {acl_action_key: acl_action}
            if acl_action == "update-event":
                scope[event_resources_access_key] = list(event_resources_access_set)
                self._emp_allowed_event_resource_access = scope[event_resources_access_key]
            scope_list.append(scope)
        return list(scope_list)




    # Resource access
    def list_emp_scopes(self, role_scopes, emp_email_id):
        # Finding all scopes blocked for the requested user
        return self.allowed_emp_scopes(role_scopes, self._emp_blocked_scope)
    
    # Resource access
    def list_emp_grant_scope_access(self, role_scopes, emp_email_id):
        # Finding all scopes blocked for the requested user to grant others
        return self.allowed_emp_scopes(role_scopes, self._emp_blocked_grant_scope)