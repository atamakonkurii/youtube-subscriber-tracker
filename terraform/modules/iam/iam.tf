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

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}