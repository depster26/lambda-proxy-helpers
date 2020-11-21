import json
from decimal import Decimal
from lambda_helpers_pkg.test_proxy_event import get_test_proxy_event
from lambda_helpers_pkg.lambda_proxy_response import LambdaProxyResponse


def test_proxy_event():
    body = {'foo': 'bar'}

    event = get_test_proxy_event(http_method='GET',
                                 resource='/test',
                                 body=body,
                                 path='/test')
    assert event['path'] == '/test'
    assert event['body'] == json.dumps(body)


def test_proxy_event_with_cognito():
    body = {'foo': 'bar'}
    cognito = {
        'user_id': 'abcdefg',
        'email': 'someone@email.com',
        'account_id': '123456'
    }

    event = get_test_proxy_event(http_method='GET',
                                 resource='/test',
                                 body=body,
                                 path='/test',
                                 cognito_detail=cognito)

    assert event['requestContext']['authorizer']['claims']['sub'] == 'abcdefg'
    assert event['requestContext']['authorizer']['claims']['cognito:username'] == 'abcdefg'
    assert event['requestContext']['authorizer']['claims']['email'] == 'someone@email.com'
    assert event['requestContext']['authorizer']['claims']['custom:account_id'] == '123456'


def test_proxy_response():
    payload = {
        'test_decimal': Decimal(3.14159265359),
        'test_string': 'abcedfgh',
        'test_bool': True,
        'test_int': 12345
    }

    resp = LambdaProxyResponse(status=200,
                               success=True,
                               payload=payload,
                               message='Test Message')

    resp_dict = resp.make_response(False)
    assert resp_dict['statusCode'] == 200

    resp_body = json.loads(resp_dict['body'])
    assert resp_body['message'] == 'Test Message'
    assert resp_body['payload']['test_string'] == 'abcedfgh'
    assert resp_body['payload']['test_decimal'] == 3.14159265359
    assert resp_body['payload']['test_bool']
    assert resp_body['payload']['test_int'] == 12345
