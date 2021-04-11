# Lambda Proxy Helpers
When I first stared exploring the serverless paradigm (on AWS) I was duplicating a fair amount code and decided it 
was high time to put it in one place so it could be shared by any serverless application I was developing. This repo 
contains a collection of utility/helper functions that I find useful when creating API's using Proxy Integration 
in API Gateway. Hopefully it'll help someone else.

## Proxy Integration in API Gateway
These helpers are specific to Proxy Integrations with API Gateway. You can find more information about proxy 
integrations [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html).

In summary, API Gateway acts purely as a proxy between the incoming request and the destination Lambda function. It 
passes all the request information to the Lambda function and expects it to handle all validations etc. API Gateway 
just expects the response to be in a very specific format passing the responsibility of constructing it to the Lambda 
function.

You can of course leverage API Gateway to parse incoming requests, pull out the relevant detail from the request,
perform validations and only send the necessary data to the Lambda function but my preference (at the time of writing) 
is not to have them so tightly coupled. I like having all the application logic in one spot to aid development and 
testing.

## Event Parser
Lambda functions accept a raw event and I wanted a single object that will abstract away all the validation 
details for me, including any required user authentication. In the main handler object, this is the first action 
that's taken:

```python
def some_handler(event, context):
    ep = EventParser(event)
    ep.validate_event_auth()
    ...
```
We instantiate a new EventParser object and hand the raw even to it. The second line calls the validate_event_auth() 
method. This will check for the existence of Cognito details in the event and will either raise an error or parse the
details out into a user_id, account_id and account_created properties of the event parser object for quick referral 
later on. If you you don't need user authentication simply omit the call to the validate function and move on.

There are other helper methods in there for retrieving body properties, path params and question string params.

### Cognito
I use AWS Cognito to handle all user management functions (no point rolling my own) and this integrates nively with API 
Gateway. You can tell the api that (certain) methods require an authenticator (of type Cognito) and it will inject 
the relevant details into the event object under the "authorizer" property.

```python
authorizer = self.event['requestContext'].get('authorizer')
claims = authorizer.get('claims')
```
From there we extract the claims component to get access to the currently logged in user. This is super handy as most
applications I write require user authentication and each user is attached to an "account". The UI doesn't have to worry
about passing the account id on requests because it's done automatically as part of the user object. All the 
API has to do is check what's being requested is associated with the account that's in the user record.

## Lambda Proxy Response
As noted above, API Gateway expects the response to be in a specific format:
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
The LambdaProxyResponse class is a utility class that handles all this for you.

> NOTE: the body of the response must be a string so any payload objects are converted as part of make_response 
> method call.

### Handling Decimals (and Dates)
One thing that comes up a lot when you have DynamoDB integration is the use of the Decimal object. As noted above the 
body of the response must be a string and json doesn't play nice with Decimals. To get around this the make_response() 
function will call do_json_compatible_replacements() on the body object before attempting to convert it to a string 
for insertion into the final response. This also handles DateTime objects.

> I pulled this solution from a discussion of the "decimal issue" here: https://github.com/boto/boto3/issues/369 

### Body Parameters
Within the body property of the response we'll either include the returned value/object OR error details. The error 
information will contain two properties:

```json
{
    "error": "...",
    "error_type": "..."
}
``` 
- _**error**_ (optional): when an exception is raised this will contain the summary error message.
- _**error_type**_ (optional): when an exception is raised this will contain the error type so the caller can check 
  this for deciding how to handle it.

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


## Function Response
This is a simple named tuple that consists of the following properties:
- _**status_code**_ - the http status code you wish to send back to the caller
- _**payload**_- the actual result you want to send back to the caller
- _**url**_ - if you created a new object and with to return a 201 status code, include the resource location of where that 
  new resource can be found here

This is the object your handler object should return when using the Lambda Proxy Wrapper.....

## Lambda Proxy Response Wrapper
This is the wrapper that pulls everything together. Simply put, if you decorate your Lambda Handler functions with this
wrapper you only need to do one of the following in your functions:

>a. return a FunctionResponse object from your handler containing the payload to return to the caller.

OR

>b. deliberately raise one of the defined errors

The wrapper will take care of constructing the correct response and catching any unhandled errors. That's it. You can 
now focus on the logic of the function(s) and not worry about constructing a valid response.

```python
@lambda_proxy_response_wrapper()
def request_handler(event, context):
    return FunctionResponse(status_code=200,
                            payload={"x": "Some parameter", "Y": "Some other parameter"},
                            url=None)
```

## Enhancements
A few things I'd like to get around to handling:
- _**integrate SNS notifications to the error handler**_ - if an unhandled error is detected an SNS message can be dispatched 
  to a topic and all subscribers will get a nicely formatted email.
- _**handle byte streams**_ - currently the proxy handler will not handle files/images etc. 



