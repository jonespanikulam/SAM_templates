import requests
import json
import boto3
from datetime import datetime, timezone, timedelta

today = datetime.now(timezone.utc)
delete_time = datetime.now(tz=timezone.utc) - timedelta(days=32)
# count=0
slack_webhook = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
s3 = boto3.client('s3')


def lambda_handler(event, context):
    print(str(event))
    count = 0
    response = s3.list_objects(Bucket='cf-templates-kr9w5lbnpxks-eu-west-1')
    for objects in response['Contents']:
        if delete_time > objects["LastModified"]:
            print(objects['Key'])
            s3.delete_object(Bucket='cf-templates-kr9w5lbnpxks-eu-west-1', Key=objects["Key"])
            count = count + 1

    print(count)
    data = str("Number of files deleted: {}".format(count))
    print(data)
    resp = requests.post(slack_webhook, json={'text': data})
    return resp.text

    # slack_message= {'text': 'Number of files deleted'}
    # resp= requests.post(slack_webhook,data=json.dumps(slack_message))
    # return resp.text
# import requests


# lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

#    return {
#        "statusCode": 200,
#        "body": json.dumps({
#            "message": "hello world",
#            # "location": ip.text.replace("\n", "")
#        }),
#    }
