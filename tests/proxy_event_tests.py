import json
from decimal import Decimal
import pytest

from lambda_proxy_helpers_pkg.test_proxy_event import get_test_proxy_event, CognitoDetail
from lambda_proxy_helpers_pkg.lambda_proxy_response import LambdaProxyResponse


@pytest.fixture()
def cognito_obj():
    return CognitoDetail(user_id='abcdef',
                         email='hello@testme.com',
                         account_id='abcdef')


def test_proxy_response_with_cognito(cognito_obj):
    body = {'foo': 'bar'}

    event = get_test_proxy_event(http_method='GET',
                                 resource='/test',
                                 body=body,
                                 path='/test',
                                 cognito_detail=cognito_obj)

    assert event['requestContext']['authorizer']['claims']['sub'] == 'abcdefg'
    assert event['requestContext']['authorizer']['claims']['cognito:username'] == 'abcdefg'
    assert event['requestContext']['authorizer']['claims']['email'] == 'someone@email.com'
    assert event['requestContext']['authorizer']['claims']['custom:account_id'] == '123456'


def test_proxy_response_body():
    payload = {
        'test_decimal': Decimal(3.14159265359),
        'test_string': 'abcedfgh',
        'test_bool': True,
        'test_int': 12345
    }

    resp = LambdaProxyResponse(status=200,
                               payload=payload)

    resp_dict = resp.make_response(False)
    assert resp_dict['statusCode'] == 200

    resp_body = json.loads(resp_dict['body'])
    assert resp_body['payload']['test_string'] == 'abcedfgh'
    assert resp_body['payload']['test_decimal'] == 3.14159265359
    assert resp_body['payload']['test_bool']
    assert resp_body['payload']['test_int'] == 12345
