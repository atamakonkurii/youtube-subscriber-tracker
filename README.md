# youtube-subscriber-tracker
* youtubeのチャンネル登録者数を取得する

### 利用技術
* Terraform
* AWS Lambda
* AWS DynamoDB
* AWS Secrets Manager
* AWS SNS
* AWS CloudWatch Event

### 利用方法

##### ⭐️aws cliでのシークレット作成
```console
aws secretsmanager create-secret \
    --name YOUTUBE_API_KEY \
    --description "YOUTUBE_API_KEY" \
    --secret-string "xxx"

aws secretsmanager create-secret \
    --name SNS_TOPIC_ARN \
    --description "SNS_TOPIC_ARN" \
    --secret-string "xxx"
```

##### ⭐️terraform.tfvarsの作成

```python
👇内容
aws_account_id = "xxx"
aws_region     = "xxx"
aws_topic_name = "xxx"
```

##### ⭐️(※必要に応じて)modules/lambda/src/constants.pyの編集
* `CHANNEL_ID`を見たいチャンネルのIDを設定するとか

##### ⭐️terraformでのビルドとデプロイ
```console
./build_and_deploy.sh
```

##### ⭐️(※必要に応じて)terraformでのリソース削除
```console
./destroy_resources.sh
```

##### ⭐️aws cliでのSNS emailのsubscription作成

```console
aws sns subscribe --topic-arn arn:aws:sns:{region}:{account_id}:{topic_name} --protocol email --notification-endpoint {email_address}
```

##### ⭐️10分ごとにLambdaが実行されるので、登録者数が変わったらメールが届く
例えばこんな感じ👇

<img src="https://github.com/atamakonkurii/youtube-subscriber-tracker/assets/71773200/c9d1228a-4f4e-4e20-83e0-d4a1eddc723a" width="320px">
