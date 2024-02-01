provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_lambda_function" "youtube_subscriber_lambda" {
  function_name     = "youtube_subscriber"
  runtime           = "python3.11"
  handler           = "lambda_function.lambda_handler"
  role              = aws_iam_role.lambda_role.arn
  source_code_hash  = filebase64sha256("../lambda/lambda_function.zip")

  // Lambda関数のソースコードを指定
  filename         = "../lambda/lambda_function.zip"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
      },
    ]
  })
}

resource "aws_iam_policy" "secret_manager_policy" {
  name        = "secret_manager_policy"
  description = "Allows access to AWS Secrets Manager"

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "secretsmanager:GetSecretValue",
        ],
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "secret_manager_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.secret_manager_policy.arn
}


resource "aws_cloudwatch_event_rule" "every_day" {
  name                = "every-day"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.every_day.name
  arn  = aws_lambda_function.youtube_subscriber_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.youtube_subscriber_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_day.arn
}