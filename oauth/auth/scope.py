from common.config import Config
common = Config()

ACL_ACTION_KEY = common.acl_action_key
ACL_ACTION_ENDPOINT_KEY = common.acl_action_endpoint
ACL_ACTION_HTTP_METHOD_KEY = common.acl_action_http_method
ACL_ACTION_DISPLAY_KEY = common.acl_action_display_key
GRANT_ACCESS_KEY = "grant-access"

def all_scope_list():
    scope_list = dict()
    scope = {}
    scope[ACL_ACTION_ENDPOINT_KEY] = "/event"
    scope[ACL_ACTION_HTTP_METHOD_KEY] = "GET"
    scope[ACL_ACTION_DISPLAY_KEY] = "Get Event"
    scope_list["get-event"] = scope

    scope = {}
    scope[ACL_ACTION_ENDPOINT_KEY] = "/event"
    scope[ACL_ACTION_HTTP_METHOD_KEY] = "POST"
    scope[ACL_ACTION_DISPLAY_KEY] = "Create Event"
    scope_list["create-event"] = scope

    scope = {}
    scope[ACL_ACTION_ENDPOINT_KEY] = "/event"
    scope[ACL_ACTION_HTTP_METHOD_KEY] = "PATCH"
    scope[ACL_ACTION_DISPLAY_KEY] = "Update Event"
    scope_list["update-event"] = scope

    scope = {}
    scope[ACL_ACTION_ENDPOINT_KEY] = "/grant"
    scope[ACL_ACTION_HTTP_METHOD_KEY] = "POST"
    scope[ACL_ACTION_DISPLAY_KEY] = "Grant access"
    scope_list[GRANT_ACCESS_KEY] = scope

    return scope_list


def list_emp_roles(emp_email_id):
    role_list = []
    role_list.append("ADMIN")
    return role_list


def list_role_scopes(role_list):
    scope_list = []
    scope_list.append("get-event")
    scope_list.append("update-event")
    scope_list.append(GRANT_ACCESS_KEY)
    return set(scope_list)


def list_emp_scopes(role_scopes, emp_email_id):
    # Finding all scopes blocked for the requested user
    blocked_scope_list = []
    blocked_scope_list.append("create-event")
    blocked_scopes = set(blocked_scope_list)
    return list(role_scopes - blocked_scopes)

def list_emp_grant_scope_access(role_scopes, emp_email_id):
    # Finding all scopes blocked for the requested user to grant others
    blocked_scope_list = []
    blocked_scope_list.append("create-event")
    blocked_scopes = set(blocked_scope_list)
    return list(role_scopes - blocked_scopes)

def list_emp_scope(emp_email_id, role_list, all_scopes):
    # Finding all scopes fall under provided role list
    role_scopes = list_role_scopes(role_list)
    # Finding all allowed scopes for the requested user
    id_token_scope_list = list_emp_scopes(role_scopes, emp_email_id)
    # Preparing the map to use in the access_token and the refresh generator as user scope detail
    access_token_scope_dict = dict()

    has_grant_access = False
    # iterating over all the allowed user scopes
    for emp_scope_key in id_token_scope_list:
        # fetching the scope detail for a specific user allowed scope
        scope_detail = all_scopes[emp_scope_key]
        scope_end_point = scope_detail[ACL_ACTION_ENDPOINT_KEY]
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
        if scope_end_point in access_token_scope_dict:
            access_token_scope_dict[scope_end_point].append(scope_detail[ACL_ACTION_HTTP_METHOD_KEY])
        else:
            access_token_scope_dict[scope_end_point] = [scope_detail[ACL_ACTION_HTTP_METHOD_KEY]]

        if emp_scope_key == GRANT_ACCESS_KEY:
            has_grant_access = True

    access_token = {"access": access_token_scope_dict}
    if has_grant_access:
        access_token["grant_access"] = list_emp_grant_scope_access(role_scopes, emp_email_id)
    return {"id_token_scope_list": id_token_scope_list, "access_token_scope": access_token}


def list_emp_scopes_from_token(payload):
    return payload[common.emp_scope_key]