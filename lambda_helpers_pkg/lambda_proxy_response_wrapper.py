import traceback
import logging
import sys
import urllib3
from functools import wraps
from . import lambda_errors
from .lambda_proxy_response import LambdaProxyResponse

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def lambda_proxy_response_wrapper(success_status_code=200):
    """
    A service wrapper that handles error handling and correct formatting of our Lambda
    function responses. Lambda function handlers can add this as a wrapper so they
    only need to make calls to the relevant methods and return a dict object. This wrapper
    will handle the correct response formatting.

    The caller provides the success code because we might want to return a 201 Created for
    example. The caller is the one who needs to indicate that. Default is set to 200 OK.

    Status code for errors are contained within the error class itself. Default is 500 Server Error.
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            resp = LambdaProxyResponse()

            try:
                result = func(*args, **kwargs)

                resp.success = True
                resp.payload = result
                resp.status = success_status_code

            except lambda_errors.InvalidFunctionRequestError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.MissingParameterError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.NotFoundError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.AlreadyExistsError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.InvalidParameterError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.RelatedRecordsExistError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.InvalidUserError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code

            except lambda_errors.GeneralError as e:
                resp.error_type = repr(e)
                resp.error = str(e.message)
                resp.status = e.status_code
                resp.event = e.event

            except urllib3.exceptions.HTTPError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                resp.error_traceback = traceback.format_exc().splitlines()
                resp.error_type = repr(type(e))
                resp.error = str(exc_value)
                resp.status = 500
                logger.error(resp.make_logging_response())

            except ValueError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                resp.error_traceback = traceback.format_exc().splitlines()
                resp.error_type = repr(type(e))
                resp.error = str(exc_value)
                resp.status = 500
                logger.error(resp.make_logging_response())

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                resp.error_traceback = traceback.format_exc().splitlines()
                resp.error_type = str(type(e))
                resp.error = str(exc_value)
                resp.status = 500
                logger.error(resp.make_logging_response())

            return resp.make_response()

        return decorated_view

    return wrapper
