import os
import json
from .lambda_errors import InvalidUserError, MissingParameterError

CUSTOM_ACCOUNT_ID = "custom:account_id"
CUSTOM_ACCOUNT_CREATED = "custom:account_created"


class EventParser:
    def __init__(self, event: dict):
        self.event = event
        self.user_id = None
        self.account_id = None
        self.account_created = None

        if self.event['body']:
            self.event_body = json.loads(self.event['body'])
        else:
            self.event_body = None

    @property
    def method(self):
        return self.event['httpMethod']

    @property
    def resource_path(self):
        return self.event['resource']

    def get_path_param(self, param_name):
        if self.event['pathParameters']:
            path_value = self.event['pathParameters'].get(param_name)

            if path_value:
                return path_value

        raise MissingParameterError(f"{param_name} not found in path parameters or value is empty")

    def get_body_prop(self, prop_name):
        if not self.event_body:
            return None

        return self.event_body.get(prop_name)

    def get_query_param(self, param_name):
        if not self.event['queryStringParameters']:
            return None

        return self.event['queryStringParameters'].get(param_name)

    def validate_event_auth(self, requires_account_id: bool = False):
        """
        Extracts the user id from the Lambda event dictionary. If the environment variable
        IS_LOCAL_DEBUG is set then it will simply use the values of environment variables TEST_USER_ID,
        TEST_ACCOUNT_ID and TEST_ACCOUNT_CREATED.

        If it's not local debug but the authorizer and/or claims properties cannot be found then an InvalidUser
        error is raised.

        :return:
        """
        is_debug = os.environ.get("IS_LOCAL_DEBUG")

        if is_debug is not None and is_debug.lower() in ('true', 1, 'y', 't'):
            self.user_id = os.environ.get("TEST_USER_ID")
            self.account_id = os.environ.get("TEST_ACCOUNT_ID")
            self.account_created = os.environ.get("TEST_ACCOUNT_CREATED") or "N"
            return

        if 'requestContext' not in self.event or not self.event['requestContext'].get('authorizer'):
            raise InvalidUserError('User invalid or not found (1)')

        authorizer = self.event['requestContext'].get('authorizer')
        claims = authorizer.get('claims')

        if not claims:
            raise InvalidUserError('User invalid or user not found (2)')

        self.user_id = claims.get('sub')

        if requires_account_id:
            self.account_id = claims.get(CUSTOM_ACCOUNT_ID)
            self.account_created = claims.get(CUSTOM_ACCOUNT_CREATED)

        if not self.user_id or (requires_account_id and not self.account_id):
            raise InvalidUserError('User invalid or not found (3)')
