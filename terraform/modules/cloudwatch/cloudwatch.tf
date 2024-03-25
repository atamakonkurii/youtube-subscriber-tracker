variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
}

variable "lambda_arn" {
  description = "Lambda ARN"
  type        = string
  
}

resource "aws_cloudwatch_event_rule" "every_day" {
  name                = "every-day"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.every_day.name
  arn  = var.lambda_arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_day.arn
}