import json
import urllib.request

import secret_manager_utils
import dynamodb_utils

def lambda_handler(event, context):
    secret_manager_youtube_api = secret_manager_utils.SecretManagerUtils("YOUTUBE_API_KEY", "ap-northeast-1")
    secret_manager_youtube_channel = secret_manager_utils.SecretManagerUtils("YOUTUBE_CHANNEL_ID", "ap-northeast-1")
    api_key = secret_manager_youtube_api._get_secret()
    channel_id = secret_manager_youtube_channel._get_secret()
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        subscriber_count_string = data['items'][0]['statistics']['subscriberCount']
        subscriber_count = int(subscriber_count_string)

        dynamodb = dynamodb_utils.DynamoDBUtils("youtube-subscriber-dynamodb-table", channel_id)

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