import yaml
import uuid
import os

# env = os.environ.get('ENV', None)
env = os.environ.get('ENV', "dev")
req_id = str(uuid.uuid4())
with open("config/config.yml", "rb") as file:
    cnf = yaml.load(file.read())

with open("config/config-" + str(env) + ".yml", "rb") as file:
    data = yaml.load(file.read())
    cnf.update(data)

def init(event):
    client_request_data = {}
    if "stageVariables" in event:
        stageVariables = event["stageVariables"]
        if stageVariables:
            for key, value in stageVariables.iteritems():
                os.environ[key] = value
    
    global cnf
    global env
    global req_id
    if "requestContext" in event:
        requestContext = event["requestContext"]
        if "stage" in requestContext:
            if "env_list" in cnf:
                if requestContext["stage"] in cnf["env_list"]:
                    env = requestContext["stage"]

        if "request_id" in requestContext:
            req_id = requestContext["request_id"]

        with open("config/config-" + str(env) + ".yml", "rb") as file:
            data = yaml.load(file.read())
            cnf.update(data)
        if "identity" in requestContext:
            requestIdentity = requestContext["identity"]
            client_request_data["sourceIp"] = requestIdentity["sourceIp"]
            client_request_data["userAgent"] = requestIdentity["userAgent"]
    return client_request_data

class Config(object):

    def get_str_property(self, property_name):
        return str(self.get_property(property_name))

    def get_property(self, property_name):
        property_value = os.environ.get(property_name, cnf[property_name])
        return property_value
    

    @property
    def google_client_id(self):
        return self.get_str_property("google_client_id")

    @property
    def ttn_oauth_url(self):
        return self.get_str_property("ttn_oauth_url")

    @property
    def hosted_domain(self):
        return self.get_str_property("hosted_domain")

    @property
    def emp_name_key(self):
        return self.get_str_property("emp_name_key")

    @property
    def emp_image_key(self):
        return self.get_str_property("emp_image_key")


    @property
    def emp_code_key(self):
        return self.get_str_property("emp_code_key")

    @property
    def acl_action_order(self):
        return self.get_str_property("acl_action_order")

    @property
    def acl_action_endpoint(self):
        return self.get_str_property("acl_action_endpoint")

    @property
    def acl_action_http_method(self):
        return self.get_str_property("acl_action_http_method")

    @property
    def acl_action_key(self):
        return self.get_str_property("acl_action_key")

    @property
    def event_resources_access_key(self):
        return self.get_str_property("event_resources_access_key")

    @property
    def acl_action_display_key(self):
        return self.get_str_property("acl_action_display_key")

    @property
    def client_id(self):
        return self.get_str_property("event_manager_app_client_id")

    @property
    def token_issuer(self):
        return self.get_str_property("token_issuer")

    @property
    def access_token_ttl_sec(self):
        return self.get_property("access_token_ttl_sec")

    @property
    def refresh_token_ttl_sec(self):
        return self.get_property("refresh_token_ttl_sec")

    @property
    def ae_algorithm(self):
        return self.get_str_property("jwt_algorithm")

    @property
    def emp_email_key(self):
        return self.get_str_property("emp_email_key")

    @property
    def emp_role_key(self):
        return self.get_str_property("emp_role_key")

    @property
    def emp_scope_key(self):
        return self.get_str_property("emp_scope_key")

    @property
    def emp_competency_key(self):
        return self.get_str_property("emp_competency_key")

    @property
    def emp_data_key(self):
        return self.get_str_property("emp_data_key")

    @property
    def client_secret(self):
        return self.get_str_property("event_manager_app_client_secret")

    @property
    def app_name(self):
        return self.get_str_property("app_name")

    # DEBUG
    # INFO
    # WARNING
    # ERROR
    @property
    def log_level(self):
        return self.get_str_property("log_level")

    @property
    def request_id(self):
        return req_id

    @property
    def id_token_secret(self):
        return self.get_str_property("id_token_secret")

    @property
    def access_token_secret(self):
        return self.get_str_property("access_token_secret")

    @property
    def encryption_salt(self):
        return self.get_str_property("encryption_salt")

    @property
    def collect_client_request_metadata(self):
        return self.get_property("collect_client_request_metadata")

    @property
    def competency_name_key(self):
        return self.get_property("competency_name_key")

    @property
    def competency_color_code_key(self):
        return self.get_property("competency_color_code_key")

    @property
    def enable_jti_encryption(self):
        return self.get_property("enable_jti_encryption")

    @property
    def internal_server_error(self):
        return "Internal Server Error"

    @property
    def un_authorize(self):
        return "Unauthorized"

    @property
    def bad_request(self):
        return "Bad Request"

    @property
    def forbidden(self):
        return "Forbidden"

    @property
    def unsupported_operation(self):
        return "Unsupported operation"
