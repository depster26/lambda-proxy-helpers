import json
import decimal


def replace_decimals(obj):
    """
    Solution from a discussion of the "decimal issue" here: https://github.com/boto/boto3/issues/369
    :param obj:
    :return:
    """
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])

        return obj

    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = replace_decimals(v)

        return obj

    elif isinstance(obj, set):
        return set(replace_decimals(i) for i in obj)

    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


class LambdaProxyResponse:
    def __init__(self,
                 status: int = 200,
                 success: bool = True,
                 payload: dict = None,
                 message: str = None):
        self.success = success
        self.message = message
        self.payload = payload
        self.status = status
        self.error = None
        self.error_type = None
        self.error_traceback = None
        self.event = None

    def __repr__(self):
        return "LambdaProxyResponse"

    def __str__(self):
        print("LambdaProxyResponse")

    def make_response(self, include_stacktrace=False, include_event=False):
        resp = {
            "statusCode": self.status,
            "headers": {
                "Content-Type": 'application/json'
            }
        }

        body = {
            "status": self.status
        }

        if self.message:
            body["message"] = self.message

        if self.payload:
            body["payload"] = replace_decimals(self.payload)

        if self.error:
            body["error"] = self.error

        if self.error_type:
            body["error_type"] = self.error_type

        if include_stacktrace and self.error_traceback:
            body["error_traceback"] = self.error_traceback

        if include_event and self.event:
            body["event"] = self.event

        resp["body"] = json.dumps(body)

        return resp

    def make_logging_response(self):
        return json.dumps(self.make_response(include_stacktrace=True,
                                             include_event=True))
