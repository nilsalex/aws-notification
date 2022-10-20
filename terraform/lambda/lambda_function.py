from datetime import datetime, timedelta
from typing import Optional

import boto3
import urllib3
import os

SUCCESS_LOCK_TYPE = 'success'
ERROR_LOCK_TYPE = 'error'


# noinspection PyUnusedLocal
def lambda_handler(event: any, context: any):
    web_page_url = event['webPageUrl']
    topic_arn = os.getenv('SNS_TOPIC_ARN')
    lock_table_name = os.getenv('LOCK_TABLE_NAME')

    print(f'web_page_url: {web_page_url}, topic_arn: {topic_arn}, lock_table_name: {lock_table_name}')

    content = get_content(web_page_url)

    if 'value="buchen"' in content:
        print('Web page contains "buchen" button!')

        if is_locked(lock_table_name, web_page_url, SUCCESS_LOCK_TYPE):
            print('Skipping notification.')
            return None

        subject = 'Freier Platz!'
        message = 'Ein freier Platz wurde gefunden! Register now:\n' + web_page_url
        notify(topic_arn, subject, message)

        set_lock(lock_table_name, web_page_url, SUCCESS_LOCK_TYPE, timedelta(hours=2))
    else:
        print('Web page does not contain a "buchen" button.')

        contains_warteliste = 'value="Warteliste"' in content
        contains_ausgebucht = 'value="ausgebucht"' in content

        if not (contains_warteliste or contains_ausgebucht):
            print('Web page does not contain a "Warteliste" or "ausgebucht" button.')
            print('Logging web page:')
            print(content)

            if is_locked(lock_table_name, web_page_url, ERROR_LOCK_TYPE):
                print('Skipping notification.')
                return None

            subject = 'Something went wrong.'
            message = 'Something went wrong, have a look at the invocation. Link to the page:\n' + web_page_url
            notify(topic_arn, subject, message)

            set_lock(lock_table_name, web_page_url, ERROR_LOCK_TYPE, timedelta(hours=2))
        else:
            print('Web page contains a "Warteliste" or "ausgebucht" button. Everything seems to work.')


def get_content(url: str) -> str:
    http = urllib3.PoolManager()
    web_page = http.request('GET', url)
    content = web_page.data.decode('utf-8')

    return content


def notify(topic_arn: str, subject: str, message: str) -> None:
    client = boto3.client('sns')
    client.publish(TopicArn=topic_arn, Subject=subject, Message=message)


def is_locked(lock_table_name: str, lock_id: str, lock_type: str) -> bool:
    if lock_time := get_lock_time(lock_table_name, lock_id, lock_type):
        return lock_time > datetime.utcnow()
    else:
        return False


def get_lock_key(lock_id: str, lock_type: str) -> str:
    return f'{lock_type}#{lock_id}'


def get_lock_time(lock_table_name: str, lock_id: str, lock_type: str) -> Optional[datetime]:
    dynamodb = boto3.client('dynamodb')

    key = get_lock_key(lock_id, lock_type)
    response = dynamodb.get_item(TableName=lock_table_name, Key={'Id': {'S': key}})

    if "Item" not in response:
        return None

    lock_timestamp = response["Item"]["Timestamp"]["S"]
    lock_time = datetime.fromisoformat(lock_timestamp)

    print(f'lock found, expires at {lock_timestamp}')

    return lock_time


def set_lock(lock_table_name: str, lock_id: str, lock_type: str, lock_expiration: timedelta) -> None:
    dynamodb = boto3.client('dynamodb')

    key = get_lock_key(lock_id, lock_type)
    lock_time = datetime.utcnow() + lock_expiration
    lock_timestamp = lock_time.isoformat()

    dynamodb.put_item(
        TableName=lock_table_name,
        Item={
            'Id': {'S': key},
            'Timestamp': {'S': lock_timestamp}
        }
    )

    print(f'lock set, expires at {lock_timestamp}')
