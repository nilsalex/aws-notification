import boto3
import os

def lambda_handler(event, context):
    topic_arn = os.getenv('SNS_TOPIC_ARN')
    message = 'hello, world!'

    client = boto3.client('sns')
    response = client.publish(TopicArn=topic_arn,Message=message)

    print(response)

