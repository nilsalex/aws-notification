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

variable "phone_number" {
  type = string
}

module "notification" {
  source = "./sns"

  phone_number = var.phone_number
}

module "lambda" {
  source = "./lambda"

  sns_topic_arn = module.notification.sns_topic_arn
}
