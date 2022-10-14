import boto3
import urllib3
import os


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    web_page_url = event['webPageUrl']
    topic_arn = os.getenv('SNS_TOPIC_ARN')

    print('web_page_url: ' + web_page_url)
    print('topic_arn: ' + topic_arn)

    http = urllib3.PoolManager()
    web_page = http.request('GET', web_page_url)
    content = web_page.data.decode('utf-8')

    if 'value="buchen"' in content:
        print('Web page contains "buchen" button!')

        subject = 'Freier Platz!'
        message = 'Ein freier Platz wurde gefunden! Register now:\n' + web_page_url

        client = boto3.client('sns')
        client.publish(TopicArn=topic_arn, Subject=subject, Message=message)
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
