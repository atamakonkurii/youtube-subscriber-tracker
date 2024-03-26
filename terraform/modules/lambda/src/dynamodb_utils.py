import boto3
import time

class DynamoDBUtils:
    def __init__(self, table_name, channel_id):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.channel_id = channel_id

    # dynamodbにデータを保存する関数
    def _put_item(self, subscriber_count):
        item = {
            'YoutubeChannelId': self.channel_id,
            'SubscriberCount': subscriber_count,
            'CreatedAt': int(time.time())
        }
        self.table.put_item(Item=item)

    def _get_latest_record(self):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('YoutubeChannelId').eq(self.channel_id),
            Limit=1,
            ScanIndexForward=False
        )

        if response['Items']:
            return response['Items'][0].get('SubscriberCount')
        else:
            return None