import traceback
from functools import wraps
from collections import namedtuple

from .constants import HttpStatusCodes
from . import lambda_errors
from .lambda_proxy_response import LambdaProxyResponse


KNOWN_ERRORS = [lambda_errors.AlreadyExistsError,
                lambda_errors.NotFoundError,
                lambda_errors.ValidationError,
                lambda_errors.MissingParameterError,
                lambda_errors.InvalidParameterError,
                lambda_errors.InvalidFunctionRequestError,
                lambda_errors.InvalidUserError,
                lambda_errors.RelatedRecordsExistError,
                lambda_errors.GeneralError]


FunctionResponse = namedtuple('FunctionResponse', ['status_code', 'payload', 'url'])


def handle_exception(e):
    if type(e) in KNOWN_ERRORS:
        return e.status_code, e.message, repr(e)
    else:
        # TODO: check for SNS notification environment vars and dispatch accordingly
        # TODO: include traceback information in the notification
        # traceback_info = traceback.format_exc().splitlines()
        return HttpStatusCodes.INTERNAL_SERVER_ERROR, f"An unhandled exception was raised: {e}", repr(e)


def lambda_proxy_response_wrapper():
    """
    A service wrapper that handles error handling and correct formatting of our Lambda
    function responses. Lambda function handlers can add this as a wrapper so they
    only need to make calls to the relevant methods and return a FunctionResponse object. This wrapper
    will handle the correct response formatting.

    Status code for errors are contained within the assigned error class itself. Unhandled exceptions
    will always raise a 500 Internal Server Error

    :return:
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            resp = LambdaProxyResponse()

            try:
                resp.status, resp.payload, resp.location = func(*args, **kwargs)

            except Exception as e:
                resp.status, resp.error, resp.error_type = handle_exception(e)

            return resp.make_response()

        return decorated_view

    return wrapper
