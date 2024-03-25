import boto3
from botocore.exceptions import ClientError

class SecretManagerUtils:
    def __init__(self, secret_name, region_name):
        self.secret_name = secret_name
        self.region_name = region_name

    # secret managerからsecretを取得する関数
    def _get_secret(self):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']

        return secret