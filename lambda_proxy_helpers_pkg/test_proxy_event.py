import json
from collections import namedtuple

CognitoDetail = namedtuple('CognitoDetail', ['user_id', 'email', 'account_id', 'account_created'])


def get_test_proxy_event(http_method: str = 'POST',
                         resource: str = '/',
                         body: dict = None,
                         path: str = '/',
                         path_params: dict = None,
                         query_string_params: dict = None,
                         stage_vars: dict = None,
                         cognito_detail: CognitoDetail = None) -> dict:
    event = {
        "resource": resource,
        "path": path,
        "httpMethod": http_method,
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": "Bearer <TOKEN>",
            "Cache-Control": "no-cache",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "User-Agent": "Custom User Agent",
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "queryStringParameters": query_string_params,
        "multiValueQueryStringParameters": None,
        "pathParameters": path_params,
        "stageVariables": stage_vars,
        "requestContext": {
            "resourceId": "abcdefghijk",
            "resourcePath": path,
            "httpMethod": http_method,
            "extendedRequestId": "abcdefghijk=",
            "requestTime": "06/Nov/2020:22:21:39 +0000",
            "path": "/Development/test",
            "accountId": "123456789",
            "protocol": "HTTP/1.1",
            "stage": "Development",
            "domainPrefix": "abcdefghi",
            "requestTimeEpoch": 1604701299694,
            "requestId": "d0550a66-2c2d-11eb-8a9f-6b193de7ce54",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "sourceIp": "127.0.0.1",
                "principalOrgId": None,
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "Custom User Agent",
                "user": None
            },
            "domainName": "1234567890.execute-api.us-east-1.amazonaws.com",
            "apiId": "abcdefghijk"
        },
        "body": json.dumps(body) if body else None,
        "isBase64Encoded": False
    }

    if cognito_detail:
        event['requestContext']['authorizer'] = {
            "claims": {
                "sub": cognito_detail.user_id,
                "aud": "1g31q8lvpfs0uqkqpravprhth5",
                "email_verified": "true",
                "event_id": "ac602ff9-b2fe-45f7-a06f-ced94764b043",
                "token_use": "id",
                "auth_time": "1604701288",
                "iss": "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_abcdef",
                "cognito:username": cognito_detail.user_id,
                "exp": "Fri Nov 06 23:21:28 UTC 2020",
                "iat": "Fri Nov 06 22:21:28 UTC 2020",
                "email": cognito_detail.email,
                "custom:account_id": cognito_detail.account_id,
                "custom:account_created": "Y" if cognito_detail.account_created else "N"
            }
        }

    return event
