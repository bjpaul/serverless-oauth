from common.config import Config
from common.logs import Log
common = Config()
log = Log()

acl_action_order = common.acl_action_order
acl_action_endpoint = common.acl_action_endpoint
acl_action_http_method = common.acl_action_http_method
acl_action_key = common.acl_action_key
event_resources_access_key = common.event_resources_access_key
acl_action_display_key = common.acl_action_display_key
grant_access_key = "grant-access"
    
class Base(object):
    # Resource access
    def all_scope_list(self):
        raise Exception(common.unsupported_operation)
    
    # Resource access
    def list_emp_roles(self, emp_email_id):
        raise Exception(common.unsupported_operation)
    
    
    # Resource access
    def list_role_scopes(self, role_list):
        raise Exception(common.unsupported_operation)
    
    def allowed_emp_scopes(self, role_scopes, blocked_scopes):
        emp_scopes = []
        for role_scope in role_scopes:
            if role_scope not in blocked_scopes:
                emp_scopes.append(role_scope)
        return emp_scopes
    
    # Resource access
    def list_emp_scopes(self, role_scopes, emp_email_id):
        raise Exception(common.unsupported_operation)
    
    # Resource access
    def list_emp_grant_scope_access(self, role_scopes, emp_email_id):
        raise Exception(common.unsupported_operation)


    def list_emp_scope(self, emp_email_id, role_list):
        all_scopes = self.all_scope_list()
        # Finding all scopes fall under provided role list
        role_scopes = self.list_role_scopes(role_list)
        # Finding all allowed scopes for the requested user
        emp_scopes = self.list_emp_scopes(role_scopes, emp_email_id)
    
        id_token_scope_list = []
        access_token_scope_dict = dict()
    
        has_grant_access = False
        # iterating over all the allowed user scopes
        for emp_scope in emp_scopes:
            emp_scope_key = emp_scope[acl_action_key]
            # fetching the scope detail for a specific user allowed scope
            scope_detail = all_scopes[emp_scope_key]
            id_token_scope = {
                acl_action_order: scope_detail[acl_action_order],
                acl_action_key: emp_scope_key,
                acl_action_display_key: scope_detail[acl_action_display_key]
            }
            scope_end_point = scope_detail[acl_action_endpoint]
            # Now, preparing the map in below form
            # "scope": {
            #     "/path1": [
            #         "POST",
            #         "GET"
            #     ],
            #     "/path2": [
            #         "POST",
            #         "PATCH"
            #     ]
            access_token_scope = {acl_action_http_method: scope_detail[acl_action_http_method]}
    
            if event_resources_access_key in emp_scope:
                id_token_scope[event_resources_access_key] = emp_scope[event_resources_access_key]
                access_token_scope[event_resources_access_key] = emp_scope[event_resources_access_key]
    
            id_token_scope_list.append(id_token_scope);
    
    
            if scope_end_point in access_token_scope_dict:
                access_token_scope_dict[scope_end_point].append(access_token_scope)
            else:
                access_token_scope_dict[scope_end_point] = [access_token_scope]
    
            if emp_scope_key == grant_access_key:
                has_grant_access = True
    
        access_token = {"access": access_token_scope_dict}
        if has_grant_access:
            access_token["grant_access"] = self.list_emp_grant_scope_access(role_scopes, emp_email_id)
        emp_scopes = {"id_token_scope_list": id_token_scope_list, "access_token_scope": access_token}
        log.debug(emp_scopes)
        return emp_scopes
    
    
    def list_emp_scopes_from_token(self, payload):
        return payload[common.emp_scope_key]