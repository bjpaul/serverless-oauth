from common.config import Config
from oauth.auth.scope.base import Base
common = Config()

acl_action_order = common.acl_action_order
acl_action_endpoint = common.acl_action_endpoint
acl_action_http_method = common.acl_action_http_method
acl_action_key = common.acl_action_key
event_resources_access_key = common.event_resources_access_key
acl_action_display_key = common.acl_action_display_key
grant_access_key = "grant-access"

class Mock(Base):
    # Resource access
    def all_scope_list(self):
        scope_list = dict()
        scope = {}
        scope[acl_action_order] = 0
        scope[acl_action_key] = "get-event"
        scope[acl_action_endpoint] = "/event"
        scope[acl_action_http_method] = "GET"
        scope[acl_action_display_key] = "Get Event"
        scope_list["get-event"] = scope
    
        scope = {}
        scope[acl_action_order] = 1
        scope[acl_action_key] = "create-event"
        scope[acl_action_endpoint] = "/event"
        scope[acl_action_http_method] = "POST"
        scope[acl_action_display_key] = "Create Event"
        scope_list["create-event"] = scope
    
        scope = {}
        scope[acl_action_order] = 2
        scope[acl_action_key] = "update-event"
        scope[acl_action_endpoint] = "/event"
        scope[acl_action_http_method] = "PATCH"
        scope[acl_action_display_key] = "Update Event"
        scope_list["update-event"] = scope
    
        scope = {}
        scope[acl_action_order] = 3
        scope[acl_action_key] = grant_access_key
        scope[acl_action_endpoint] = "/grant"
        scope[acl_action_http_method] = "POST"
        scope[acl_action_display_key] = "Grant access"
        scope_list[grant_access_key] = scope
    
        return scope_list
    
    # Resource access
    def list_emp_roles(self, emp_email_id):
        role_list = []
        role_list.append("ADMIN")
        return role_list
    
    
    # Resource access
    def list_role_scopes(self, role_list):
        scope_list = []
        scope_list.append({acl_action_key:"get-event"})
        event_resources_access_list = "update-event-slot,update-event-location,update-event-competency,update-event-agenda"
        scope_list.append({acl_action_key: "update-event", event_resources_access_key:event_resources_access_list.split(",")})
        scope_list.append({acl_action_key:grant_access_key})
        return scope_list
    
    # Resource access
    def list_emp_scopes(self, role_scopes, emp_email_id):
        # Finding all scopes blocked for the requested user
        blocked_scope_list = []
        blocked_scope_list.append("create-event")
        return self.allowed_emp_scopes(role_scopes, blocked_scope_list)
    
    # Resource access
    def list_emp_grant_scope_access(self, role_scopes, emp_email_id):
        # Finding all scopes blocked for the requested user to grant others
        blocked_scope_list = []
        blocked_scope_list.append("create-event")
        return self.allowed_emp_scopes(role_scopes, blocked_scope_list)