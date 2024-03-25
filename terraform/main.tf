provider "aws" {
  region = "ap-northeast-1"
}

module "iam" {
  source = "./modules/iam"
  aws_account_id = var.aws_account_id
  aws_region = var.aws_region
}

module "lambda" {
  source = "./modules/lambda"
  lambda_role_arn = module.iam.lambda_role_arn
}

module "cloudwatch" {
  source = "./modules/cloudwatch"
  lambda_function_name = module.lambda.lambda_function_name
  lambda_arn = module.lambda.lambda_arn
}

module "dynamodb" {
  source = "./modules/dynamodb"
}