import json
import urllib.request
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    api_key = __get_secret("YOUTUBE_API_KEY")
    channel_id = __get_secret("YOUTUBE_CHANNEL_ID")
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        subscriber_count = data['items'][0]['statistics']['subscriberCount']

        item = {
            'YoutubeChannelId': channel_id,
            'SubscriberCount': int(subscriber_count)
        }
        __put_item(item)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Subscriber count: {subscriber_count}")
    }

# secret managerからsecretを取得する関数
def __get_secret(secret_name):

    secret_name = secret_name
    region_name = "ap-northeast-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return secret

# dynamodbにデータを保存する関数
def __put_item(item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('youtube-subscriber-dynamodb-table')
    table.put_item(Item=item)