import json
import urllib.request
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    api_key = _get_secret("YOUTUBE_API_KEY")
    channel_id = _get_secret("YOUTUBE_CHANNEL_ID")
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        subscriber_count_string = data['items'][0]['statistics']['subscriberCount']
        subscriber_count = int(subscriber_count_string)

        previous_subscriber_count = _get_latest_record(channel_id)

        if previous_subscriber_count > subscriber_count:
            print("Subscriber count is decreasing.")
            _put_item(channel_id, subscriber_count)
        elif previous_subscriber_count < subscriber_count:
            print("Subscriber count is increasing.")
            _put_item(channel_id, subscriber_count)
        else:
            print("Subscriber count is not changed.")
            return {
                'statusCode': 200,
        'body': json.dumps(f"Subscriber count is not changed.")
            }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Subscriber count: {subscriber_count_string}")
    }

# secret managerからsecretを取得する関数
def _get_secret(secret_name):

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
def _put_item(channel_id, subscriber_count):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(_dynamodb_table_name)

    item = {
        'YoutubeChannelId': channel_id,
        'SubscriberCount': subscriber_count
    }
    table.put_item(Item=item)

def _get_latest_record(channel_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(_dynamodb_table_name)

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('YoutubeChannelId').eq(channel_id),
        Limit=1,
        ScanIndexForward=False
    )

    if response['Items']:
        return response['Items'][0].get('SubscriberCount')
    else:
        return None
    
_dynamodb_table_name = "youtube-subscriber-dynamodb-table"