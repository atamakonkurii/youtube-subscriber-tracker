import json
import urllib.request

from secret_manager_utils import SecretManagerUtils
from dynamodb_utils import DynamoDBUtils
from sns_utils import SNSUtils
from constants import REGION, CHANNEL_ID, DYNAMODB_TABLE_NAME, YOUTUBE_API_SECRET_NAME


def lambda_handler(event, context):
    # YouTube APIキーをSecretManagerから取得
    youtube_api_key = __get_youtube_api_key()

    # YouTube DATA APIからチャンネル登録者数を取得
    subscriber_count = __fetch_subscriber_count(youtube_api_key)

    # 前回保存したチャンネル登録者数をDynamoDBから取得
    previous_subscriber_count = __get_previous_subscriber_count()

    # チャンネル登録者数を比較して、SNSトピックにメッセージを送信し、DynamoDBにチャンネル登録者数を保存
    # 登録者が変わっていない場合は何もしない
    return __save_and_publish_subscriber(subscriber_count, previous_subscriber_count)
        
def __get_youtube_api_key():
    secret_manager_youtube_api = SecretManagerUtils(YOUTUBE_API_SECRET_NAME, REGION)
    api_key = secret_manager_youtube_api._get_secret()
    return api_key

def __fetch_subscriber_count(api_key):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        subscriber_count_string = data['items'][0]['statistics']['subscriberCount']
        subscriber_count = int(subscriber_count_string)
        return subscriber_count
    
def __get_previous_subscriber_count():
    dynamodb = DynamoDBUtils(DYNAMODB_TABLE_NAME, CHANNEL_ID)
    previous_subscriber_count = dynamodb._get_latest_record()
    return previous_subscriber_count

        
def __save_and_publish_subscriber(subscriber_count, previous_subscriber_count):
    # チャンネル登録者が変わっていない場合は早期リターン
    if previous_subscriber_count == subscriber_count:
        return {
            'statusCode': 200,
            'body': json.dumps(f"Subscriber count is not changed.")
        }
    
    # チャンネル登録者数をDynamoDBに保存
    dynamodb = DynamoDBUtils(DYNAMODB_TABLE_NAME, CHANNEL_ID)
    dynamodb._put_item(subscriber_count)

    # チャンネル登録者数の変化に応じてSNSトピックにメッセージを送信
    if previous_subscriber_count > subscriber_count:
        return __publish_message(f"残念！登録者が減ったよ、、、\n登録者： {subscriber_count}({subscriber_count - previous_subscriber_count})")
    elif previous_subscriber_count < subscriber_count:
        return __publish_message(f"おめでとう登録者が増えたよ！\n登録者： {subscriber_count}(+{subscriber_count - previous_subscriber_count})")

def __publish_message(message):
    SNSUtils()._publish_message(message)
    return {
        'statusCode': 200,
        'body': json.dumps(f"Sent message: {message}")
    }