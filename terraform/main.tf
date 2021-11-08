terraform {
  backend "s3" {
    region         = "eu-central-1"
    key            = "aws-notification.tfstate"
    bucket         = "nalex-state-bucket"
    dynamodb_table = "state-lock-table"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.63"
    }
    archive = {}
  }
}

variable "email_address" {
  type = string
}

module "notification" {
  source = "./sns"

  email_address = var.email_address
}

module "lambda" {
  source = "./lambda"

  sns_topic_arn = module.notification.sns_topic_arn
}

module "trigger" {
  source = "./eventbridge"

  lambda_function_name = module.lambda.lambda_function_name
}
