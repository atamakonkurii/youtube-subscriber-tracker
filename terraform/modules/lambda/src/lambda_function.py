import json
import urllib.request

from secret_manager_utils import SecretManagerUtils
from dynamodb_utils import DynamoDBUtils

def lambda_handler(event, context):
    region = "ap-northeast-1"
    secret_manager_youtube_api = SecretManagerUtils("YOUTUBE_API_KEY", region)
    secret_manager_youtube_channel = SecretManagerUtils("YOUTUBE_CHANNEL_ID", region)
    
    api_key = secret_manager_youtube_api._get_secret()
    channel_id = secret_manager_youtube_channel._get_secret()
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        subscriber_count_string = data['items'][0]['statistics']['subscriberCount']
        subscriber_count = int(subscriber_count_string)

        dynamodb = DynamoDBUtils("youtube-subscriber-dynamodb-table", channel_id)

        previous_subscriber_count = dynamodb._get_latest_record()

        if previous_subscriber_count > subscriber_count:
            print("Subscriber count is decreasing.")
            dynamodb._put_item(subscriber_count)
        elif previous_subscriber_count < subscriber_count:
            print("Subscriber count is increasing.")
            dynamodb._put_item(subscriber_count)
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