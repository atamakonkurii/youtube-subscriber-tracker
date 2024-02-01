# youtube-subscriber-tracker
* youtubeのチャンネル登録者数を取得する

```
# aws cliでのシークレット作成

aws secretsmanager create-secret \
    --name YOUTUBE_API_KEY \
    --description "YOUTUBE_API_KEY" \
    --secret-string "xxx"

aws secretsmanager create-secret \
    --name YOUTUBE_CHANNEL_ID \
    --description "YOUTUBE_CHANNEL_ID" \
    --secret-string "xxx"
```