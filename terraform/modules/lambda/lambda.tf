variable "lambda_role_arn" {
  description = "Lambda role ARN"
  type        = string
}

resource "aws_lambda_function" "youtube_subscriber_lambda" {
  function_name    = "youtube_subscriber"
  runtime          = "python3.11"
  handler          = "lambda_function.lambda_handler"
  timeout          = 10
  role             = var.lambda_role_arn
  source_code_hash = filebase64sha256("${path.module}/src/lambda_function.zip")
  filename         = "${path.module}/src/lambda_function.zip"
}

output "lambda_function_name" {
  value = aws_lambda_function.youtube_subscriber_lambda.function_name
}

output "lambda_arn" {
  value = aws_lambda_function.youtube_subscriber_lambda.arn
}