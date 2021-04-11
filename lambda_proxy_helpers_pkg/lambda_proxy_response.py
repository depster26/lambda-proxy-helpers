import json
from datetime import datetime
from decimal import Decimal


def do_json_compatible_replacements(obj):
    """
    Solution from a discussion of the "decimal issue" here: https://github.com/boto/boto3/issues/369
    :param obj:
    :return:
    """
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = do_json_compatible_replacements(obj[i])

        return obj

    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = do_json_compatible_replacements(v)

        return obj

    elif isinstance(obj, set):
        return set(do_json_compatible_replacements(i) for i in obj)

    elif isinstance(obj, datetime):
        return obj.isoformat()

    elif isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


class LambdaProxyResponse:
    def __init__(self,
                 status: int = 200,
                 payload: dict = None,
                 location: str = None,
                 error=None,
                 error_traceback=None):
        self.payload = payload
        self.status = status
        self.error = error
        self.error_traceback = error_traceback
        self.location = location

    def __repr__(self):
        return f"LambdaProxyResponse(status={self.status}," \
               f"payload={self.payload}, " \
               f"location={self.location}, " \
               f"error={self.error}, " \
               f"error_traceback={self.error_traceback})"

    def __str__(self):
        print("LambdaProxyResponse")

    def make_response(self, include_stacktrace=False):
        """
        The response body will contain one of the following:
            - empty
            - the payload provided by the caller
            - details of the error generated

        NOTE: this doesn't (yet) include isBase64Encoded so won't work with files, images etc.
        """
        resp = {
            "statusCode": self.status,
            "headers": {
                "Content-Type": 'application/json',
                "Access-Control-Allow-Origin": '*',
                "Access-Control-Allow-Credentials": True
            }
        }

        tmp_payload = None

        if self.error:
            tmp_payload = {
                "error": self.error
            }

            if include_stacktrace and self.error_traceback:
                tmp_payload["errorTraceback"] = self.error_traceback

        else:
            if self.payload:
                tmp_payload = self.payload

            if self.location:
                resp['headers']['Location'] = self.location

        resp["body"] = do_json_compatible_replacements(tmp_payload)

        return resp

    def make_logging_response(self):
        return json.dumps(self.make_response(include_stacktrace=True))