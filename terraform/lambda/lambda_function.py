from datetime import datetime

import boto3
import urllib3
import os


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    web_page_url = event['webPageUrl']
    topic_arn = os.getenv('SNS_TOPIC_ARN')
    lock_table_name = os.getenv('LOCK_TABLE_NAME')

    print('web_page_url: ' + web_page_url)
    print('topic_arn: ' + topic_arn)
    print('lock_table_name: ' + lock_table_name)

    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(TableName=lock_table_name, Key={'Id': {'S': web_page_url}})

    if "Item" in response:
        lock_timestamp = response["Item"]["Timestamp"]["S"]
        lock_time = datetime.fromisoformat(lock_timestamp)
        now = datetime.utcnow()

        print('Lock found')
        print('lock time: ' + str(lock_time))
        print('now time: ' + str(now))

        if (now - lock_time).total_seconds() < 1800:
            print('lock expires in ' + str(1800 - (now - lock_time).total_seconds()) + ' seconds')
            print('skipping')
            return

    http = urllib3.PoolManager()
    web_page = http.request('GET', web_page_url)
    content = web_page.data.decode('utf-8')

    if 'value="buchen"' in content:
        print('Web page contains "buchen" button!')

        subject = 'Freier Platz!'
        message = 'Ein freier Platz wurde gefunden! Register now:\n' + web_page_url

        client = boto3.client('sns')
        client.publish(TopicArn=topic_arn, Subject=subject, Message=message)

        response = dynamodb.put_item(
            TableName=lock_table_name,
            Item={
                'Id': {'S': web_page_url},
                'Timestamp': {'S': datetime.utcnow().isoformat()}
            }
        )
    else:
        print('Web page does not contain a "buchen" button.')

        contains_warteliste = 'value="Warteliste"' in content
        contains_ausgebucht = 'value="ausgebucht"' in content

        if not (contains_warteliste or contains_ausgebucht):
            print('Web page does not contain a "Warteliste" or "ausgebucht" button.')
            print('Logging web page.')
            print(content)

            subject = 'Something went wrong.'
            message = 'Something went wrong, have a look at the invocation. Link to the page:\n' + web_page_url

            client = boto3.client('sns')
            client.publish(TopicArn=topic_arn, Subject=subject, Message=message)
        else:
            print('Web page contains a "Warteliste" or "ausgebucht" button. Everything seems to work.')
