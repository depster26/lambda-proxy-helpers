# Lambda Helpers (Python)
When exploring the serverless paradigm (on AWS) I was duplicating a fair amount code and decided it was time to put it 
in one spot so it could be shared by any serverless application. This repo contains a collection of utility/helper 
functions that I find useful.

## lambda_proxy_response.py
Helper class for managing the expected response to be returned to Lambda and ultimately API Gateway. When using API 
Gateway proxy integration to call a Lambda function the response must be formatted like this:  

```json
{
    "isBase64Encoded": false,
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "..."
}
```
This helper class handles it for you by populating with the relevant properties and calling make_response().

> the body of the response must be a string so the dictionary is converted as part of make_response.

### Handling Decimals
One thing that comes up a lot when you have DynamoDB integration is the use of the Decimal object. As noted above the 
body of the response must be a string and json doesn't play nice with Decimals. To get  around this the make_response() 
function will call replace_decimals() on the body object before attempting to convert it to a string for insertion 
into the final response.

> I pulled this solution from a discussion of the "decimal issue" here: https://github.com/boto/boto3/issues/369 

### Body Parameters
Within the body property of the response I include the following properties:
```json
{
    "status": 200,
    "message": "...",
    "payload": "...",
    "error": "...",
    "error_type": "..."
}
``` 
- _**status**_ (always present): the same status code as set in the actual response object in case I need access to it.
- _**message**_ (optional): sometimes I don't need a payload dictionary but just a feedback message.
- _**payload**_ (optional): the main part of the response that includes whatever dictionary you need to send back to 
the caller.
- _**error**_ (optional): when an exception is raised this will contain the summary error message.
- _**error_type**_ (optional): when an exception is raised this will contain the the error type.

There are two additional parameters that get added to this response when logging is triggered:

```json
{
    "event": "...",
    "error_traceback": "..."
}
```
- _**event**_ (optional): if I need to raise an error I can also include the incoming event object to aid debugging.
- _**error_traceback**_ (optional): for "unhandled" exceptions this will contain the traceback.

> I never want to send these two pieces of information to the function caller but they provide a lot of useful 
>information when attempting to debug errors. When logging unhandled and general exceptions I'll log the response 
>along with these by invoking make_logging_response().

## lambda_proxy_response_wrapper.py
When writing Lambda functions for use with API Gateway using the proxy integration this wrapper function handles
the correct response format Lambda is expecting. The handler function simply needs to focus on the body of the 
response and return a dict/string/list etc. Simply decorate the handler method as such:

```python
@lambda_proxy_response_wrapper()
def request_handler(event, context):
    return {"x": "Some parameter", "Y": "Some other parameter"}
```

### Error handling
The wrapper handles any known (and unknown) errors thrown by the function. For known errors (see 
lambda_errors.py below) it will set the correct error information in the response and return the appropriate status 
code. For unknown errors it will do the same but also log the stack trace to aid debugging.

## lambda_errors.py
Contains a set of "custom" exception classes that can be raised by the handler functions:

- _**NotFoundError**_: when the item requested is not found
- _**MissingParameterError**_: a required parameter has been omitted
- _**InvalidParameterError**_: an invalid parameter has been provided
- _**AlreadyExistsError**_: when an item being added (to whatever) already exists and shouldn’t be overwritten.
- _**RelatedRecordsExist**_: if an object is being deleted but related items exist. User should remove the related items 
before attempting a delete on the parent.
- _**ValidationError**_: when a validation attempt fails
- _**InvalidFunctionRequestError**_: if the handler method is unable to determine what function to call
- _**InvalidUserError**_: if the user cannot be found or expected user attributes are not part of the request event
- _**GeneralError**_: alias to the base Exception object but you can include the event object for debugging

