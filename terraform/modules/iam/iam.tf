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
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
        ],
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:*"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_dynamodb_access" {
  name        = "lambda_dynamodb_access"
  description = "Allow lambda function to access DynamoDB"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        "Resource" : "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/youtube-subscriber-dynamodb-table"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_sns_publish" {
  name        = "lambda_sns_publish"
  description = "Allow lambda function to publish to SNS topic"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "sns:Publish",
        Resource = "arn:aws:sns:${var.aws_region}:${var.aws_account_id}:${var.aws_topic_name}"
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "secret_manager_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.secret_manager_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_dynamodb_access.arn
}

resource "aws_iam_role_policy_attachment" "lambda_sns_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_sns_publish.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}