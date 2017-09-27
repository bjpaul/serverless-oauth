import yaml
import uuid
import os


class Config(object):
    def __init__(self):
        self._env = os.environ.get('ENV', None)
        if not self._env:
            raise ValueError('You must have set "ENV" variable')

        with open("config/config.yml", "rb") as config:
            self._config = yaml.load(config.read())

        with open("config/config-"+str(self._env)+".yml", "rb") as config:
            data = yaml.load(config.read())
            self._config.update(data)
        self._req_id = str(uuid.uuid4())


    def get_str_property(self, property_name):
        return str(self.get_property(property_name))

    def get_property(self, property_name):
        property_value = os.environ.get(property_name, None)
        if not property_value:
            # if property_name not in self._config.keys():  # we don't want KeyError
            #     return None  # just return None if not found
            return self._config[property_name]
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
    def google_user_id_key(self):
        return self.get_str_property("google_user_id_key")

    @property
    def emp_code_key(self):
        return self.get_str_property("emp_code_key")

    @property
    def acl_action_key(self):
        return self.get_str_property("acl_action_key")

    @property
    def acl_action_endpoint(self):
        return self.get_str_property("acl_action_endpoint")

    @property
    def acl_action_http_method(self):
        return self.get_str_property("acl_action_http_method")

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
    def emp_roll_key(self):
        return self.get_str_property("emp_roll_key")

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
    def pem_passphrase(self):
        return self.get_str_property("pem_passphrase")

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
        return self._req_id

    @property
    def encryption_key(self):
        return self.get_str_property("encryption_key")

    @property
    def id_token_private_key(self):
        if self._env == "dev":
            with open(self.get_str_property("id_token_private_pem"), "rb") as pemfile:
                return pemfile.read()
        else:
            # TODO: Download from S3
            return os.environ.get('id_token_private_key', None)

    @property
    def access_token_private_key(self):
        if self._env == "dev":
            with open(self.get_str_property("access_token_private_pem"), "rb") as pemfile:
                return pemfile.read()
        else:
            # TODO: Download from S3
            return os.environ.get('access_token_private_key', None)

    @property
    def access_token_public_key(self):
        if self._env == "dev":
            with open(self.get_str_property("access_token_public_pem"), "rb") as pemfile:
                return pemfile.read()
        else:
            # TODO: Download from S3
            return os.environ.get('access_token_public_key', None)