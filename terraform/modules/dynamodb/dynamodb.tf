resource "aws_dynamodb_table" "youtube-subscriber-dynamodb-table" {
  name         = "youtube-subscriber-dynamodb-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "YoutubeChannelId"
  range_key    = "SubscriberCount"

  attribute {
    name = "YoutubeChannelId"
    type = "S"
  }

  attribute {
    name = "SubscriberCount"
    type = "N"
  }
}