import json
import urllib.request

from secret_manager_utils import SecretManagerUtils
from dynamodb_utils import DynamoDBUtils
from sns_utils import SNSUtils
from constants import REGION, CHANNEL_ID, DYNAMODB_TABLE_NAME


def lambda_handler(event, context):
    secret_manager_youtube_api = SecretManagerUtils("YOUTUBE_API_KEY", REGION)
    api_key = secret_manager_youtube_api._get_secret()

    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        subscriber_count_string = data['items'][0]['statistics']['subscriberCount']
        subscriber_count = int(subscriber_count_string)

        dynamodb = DynamoDBUtils(DYNAMODB_TABLE_NAME, CHANNEL_ID)

        previous_subscriber_count = dynamodb._get_latest_record()

        if previous_subscriber_count > subscriber_count:
            dynamodb._put_item(subscriber_count)
            SNSUtils()._publish_message(f"残念！登録者が減ったよ、、、\n登録者： {subscriber_count}({subscriber_count - previous_subscriber_count})")
        elif previous_subscriber_count < subscriber_count:
            dynamodb._put_item(subscriber_count)
            SNSUtils()._publish_message(f"おめでとう登録者が増えたよ！\n登録者： {subscriber_count}(+{subscriber_count - previous_subscriber_count})")
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(f"Subscriber count is not changed.")
            }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Subscriber count: {subscriber_count_string}")
    }