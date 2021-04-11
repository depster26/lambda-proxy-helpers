import pytest
import json

from lambda_proxy_helpers_pkg.constants import HttpStatusCodes
from lambda_proxy_helpers_pkg.lambda_proxy_response_wrapper import lambda_proxy_response_wrapper
from lambda_proxy_helpers_pkg.lambda_errors import (NotFoundError,
                                                    MissingParameterError,
                                                    InvalidParameterError,
                                                    InvalidFunctionRequestError,
                                                    InvalidUserError,
                                                    AlreadyExistsError,
                                                    RelatedRecordsExistError,
                                                    GeneralError,
                                                    ValidationError)

PROP_STATUS = 'statusCode'
PROP_BODY = 'body'
PROP_ERROR = 'error'
PROP_ERROR_TYPE = 'errorType'


def test_unhandled_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        i = 0 / 0

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.INTERNAL_SERVER_ERROR
    body = json.loads(resp[PROP_BODY])
    assert 'unhandled exception' in body[PROP_ERROR]
    assert 'division by zero' in body[PROP_ERROR_TYPE]


def test_not_found_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise NotFoundError("Invalid user or user not found")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.NOT_FOUND

    body = json.loads(resp[PROP_BODY])
    assert 'Invalid user' in body[PROP_ERROR]
    assert 'Not Found Error' == body[PROP_ERROR_TYPE]


def test_missing_param_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise MissingParameterError("Parameter X is missing")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'X is missing' in body[PROP_ERROR]
    assert 'Missing Parameter Error' == body[PROP_ERROR_TYPE]


def test_invalid_param_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise InvalidParameterError("Param X is invalid or missing")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'invalid or missing' in body[PROP_ERROR]
    assert 'Invalid Parameter Error' == body[PROP_ERROR_TYPE]


def test_record_exists_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise AlreadyExistsError("Record already exists")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'already exists' in body[PROP_ERROR]
    assert 'Object Already Exists Error' == body[PROP_ERROR_TYPE]


def test_related_records_exist_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise RelatedRecordsExistError("Record cannot be deleted as related records exist")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'cannot be deleted' in body[PROP_ERROR]
    assert 'Related Records Exist Error' == body[PROP_ERROR_TYPE]


def test_validation_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise ValidationError("Was unable to validate the input parameter")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'unable to validate' in body[PROP_ERROR]
    assert 'Validation Error' == body[PROP_ERROR_TYPE]


def test_invalid_function_request_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise InvalidFunctionRequestError("Cannot determine the function to execute")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'determine the function' in body[PROP_ERROR]
    assert 'Invalid Function Request Error' == body[PROP_ERROR_TYPE]


def test_invalid_user_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise InvalidUserError("User is invalid or user cannot be found")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.BAD_REQUEST

    body = json.loads(resp[PROP_BODY])
    assert 'is invalid or user' in body[PROP_ERROR]
    assert 'Invalid User Error' == body[PROP_ERROR_TYPE]


def test_general_error_response():
    @lambda_proxy_response_wrapper()
    def test_function():
        raise GeneralError("A general error was raised")

    resp = test_function()
    assert resp[PROP_STATUS] == HttpStatusCodes.INTERNAL_SERVER_ERROR

    body = json.loads(resp[PROP_BODY])
    assert 'general error was raised' in body[PROP_ERROR]
    assert 'General Error' == body[PROP_ERROR_TYPE]
