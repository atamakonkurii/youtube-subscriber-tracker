variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
}

variable "lambda_arn" {
  description = "Lambda ARN"
  type        = string

}

resource "aws_cloudwatch_event_rule" "every_10_minutes" {
  name                = "every_10_minutes"
  schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.every_10_minutes.name
  arn  = var.lambda_arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_10_minutes.arn
}