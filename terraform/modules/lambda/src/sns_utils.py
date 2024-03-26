import boto3

from secret_manager_utils import SecretManagerUtils
from constants import REGION, SNS_TOPIC_ARN_SECRET_NAME

class SNSUtils:
    def __init__(self):
        self.sns = boto3.client('sns')
        secret_manager_sns_topic_arn = SecretManagerUtils(SNS_TOPIC_ARN_SECRET_NAME, REGION)
        sns_topic_arn = secret_manager_sns_topic_arn._get_secret()
        self.topic_arn = sns_topic_arn

    # SNSトピックにメッセージを送信する関数
    def _publish_message(self, message):
        self.sns.publish(
            TopicArn=self.topic_arn,
            Message=message,
            Subject="【チャンネル登録者増減お知らせ】"
        )