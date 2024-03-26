# youtube-subscriber-tracker
* youtubeのチャンネル登録者数を取得する

```
# aws cliでのシークレット作成

aws secretsmanager create-secret \
    --name YOUTUBE_API_KEY \
    --description "YOUTUBE_API_KEY" \
    --secret-string "xxx"

aws secretsmanager create-secret \
    --name SNS_TOPIC_ARN \
    --description "SNS_TOPIC_ARN" \
    --secret-string "xxx"
```

```
# aws cliでのSNS emailのsubscription作成
aws sns subscribe --topic-arn arn:aws:sns:{region}:{account_id}:{topic_name} --protocol email --notification-endpoint {email_address}
```

aws sns subscribe --topic-arn arn:aws:sns:ap-northeast-1:321462977814:youtube-subscribe-notify-topic --protocol email --notification-endpoint atamakonkurii.kazuki@gmail.com