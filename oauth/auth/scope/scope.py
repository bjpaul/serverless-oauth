from common import config
from oauth.auth.scope.mock import Mock
from oauth.auth.scope.db import DynamoDB


def provider():
    if config.env == "dev":
        return Mock()
    else:
        return DynamoDB()
