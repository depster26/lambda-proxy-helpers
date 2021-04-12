import pytest

from lambda_proxy_helpers_pkg.lambda_errors import InvalidUserError, MissingParameterError
from lambda_proxy_helpers_pkg.test_proxy_event import get_test_proxy_event, CognitoDetail
from lambda_proxy_helpers_pkg.event_parser import EventParser


@pytest.fixture()
def cognito_obj():
    return CognitoDetail(user_id='abcdef',
                         email='hello@testme.com',
                         account_id='abcdef')


def test_user_is_none():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test',
                                      body=None,
                                      path='/test',
                                      cognito_detail=None)

    event_parser = EventParser(event=test_event)

    with pytest.raises(InvalidUserError) as e:
        event_parser.validate_event_auth(requires_account_id=True)

    assert "User invalid" in e.value.message


def test_missing_user():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test',
                                      body=None,
                                      path='/test',
                                      cognito_detail=CognitoDetail(user_id=None,
                                                                   email=None,
                                                                   account_id=None))

    event_parser = EventParser(event=test_event)

    with pytest.raises(InvalidUserError) as e:
        event_parser.validate_event_auth(requires_account_id=True)

    assert "User invalid" in e.value.message


def test_missing_account_id():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test',
                                      body=None,
                                      path='/test',
                                      cognito_detail=CognitoDetail(user_id='abcdef',
                                                                   email=None,
                                                                   account_id=None))

    event_parser = EventParser(event=test_event)

    with pytest.raises(InvalidUserError) as e:
        event_parser.validate_event_auth(requires_account_id=True)

    assert "User invalid" in e.value.message


def test_get_body_prop():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body={"foo": "bar"},
                                      path='/test/123',
                                      path_params={"testId": 123})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_body_prop('foo') == 'bar'


def test_get_body_prop_empty():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body={"foo": None},
                                      path='/test/123',
                                      path_params={"testId": 123})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_body_prop('foo') is None


def test_get_body_prop_missing():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body={"foo": None},
                                      path='/test/123',
                                      path_params={"testId": 123})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_body_prop('bar') is None


def test_get_query_param_empty():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body={"foo": None},
                                      path='/test/123',
                                      path_params={"testId": 123})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_query_param('amIHere') is None


def test_get_query_param():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body={"foo": None},
                                      path='/test/123',
                                      path_params={"testId": 123},
                                      query_string_params={"amIHere": "Yes"})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_query_param('amIHere') == "Yes"


def test_get_query_param_is_none():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body={"foo": None},
                                      path='/test/123',
                                      path_params={"testId": 123},
                                      query_string_params={"amIHere": None})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_query_param('amIHere') is None


def test_get_path_param():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body=None,
                                      path='/test/123',
                                      path_params={"testId": 123})

    event_parser = EventParser(event=test_event)
    assert event_parser.get_path_param('testId') == 123


def test_get_path_param_empty():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body=None,
                                      path='/test/123',
                                      path_params={"testId": ""})

    event_parser = EventParser(event=test_event)

    with pytest.raises(MissingParameterError) as e:
        event_parser.get_path_param('testId')

    assert 'testId not found' in e.value.message


def test_get_path_param_missing():
    test_event = get_test_proxy_event(http_method='GET',
                                      resource='/test/:testId',
                                      body=None,
                                      path='/test/123',
                                      path_params=None)

    event_parser = EventParser(event=test_event)

    with pytest.raises(MissingParameterError) as e:
        event_parser.get_path_param('testId')

    assert 'testId not found' in e.value.message
