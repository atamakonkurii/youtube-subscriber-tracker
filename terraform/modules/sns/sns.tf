resource "aws_sns_topic" "youtube-subscribe-notify-topic" {
  name = var.aws_topic_name
}