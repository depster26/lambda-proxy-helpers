from lambda_proxy_helpers_pkg.lambda_proxy_response_wrapper import handle_exception
from lambda_proxy_helpers_pkg.lambda_errors import (NotFoundError,
                                                    MissingParameterError,
                                                    InvalidParameterError,
                                                    InvalidFunctionRequestError,
                                                    InvalidUserError,
                                                    AlreadyExistsError,
                                                    RelatedRecordsExistError,
                                                    GeneralError,
                                                    ValidationError)
from lambda_proxy_helpers_pkg.constants import HttpStatusCodes


def test_not_found_error():
    error_message = "Param was not found"
    e = NotFoundError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.NOT_FOUND
    assert message == error_message


def test_missing_param_error():
    error_message = "Testing the missing parameter error"
    e = MissingParameterError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.BAD_REQUEST
    assert message == error_message


def test_invalid_param_error():
    error_message = "Invalid Param was given"
    e = InvalidParameterError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.BAD_REQUEST
    assert message == error_message


def test_already_exists_error():
    error_message = "Record already exists"
    e = AlreadyExistsError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.BAD_REQUEST
    assert message == error_message


def test_related_records_exists_error():
    error_message = "Related records already exist"
    e = RelatedRecordsExistError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.BAD_REQUEST
    assert message == error_message


def test_validation_error():
    error_message = "Something went wrong with the validations"
    e = ValidationError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.BAD_REQUEST
    assert message == error_message


def test_invalid_user_error():
    error_message = "Invalid user"
    e = InvalidUserError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.NOT_FOUND
    assert message == error_message


def test_invalid_function_request_error():
    error_message = "Invalid function request"
    e = InvalidFunctionRequestError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.BAD_REQUEST
    assert message == error_message


def test_general_error():
    error_message = "Something really bad happened"
    e = GeneralError(error_message)

    status, message = handle_exception(e)

    assert status == HttpStatusCodes.INTERNAL_SERVER_ERROR
    assert message == error_message
