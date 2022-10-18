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

variable "email_addresses" {
  type = list(string)
}

module "notification" {
  source = "./sns"

  email_addresses = var.email_addresses
}

module "table" {
  source = "./dynamodb"

  table_name = "notification-lambda-state-table"
}

module "lambda" {
  source = "./lambda"

  sns_topic_arn      = module.notification.sns_topic_arn
  dynamodb_table_arn = module.table.dynamodb_table_arn
}

module "trigger_volleyball" {
  source = "./trigger"

  trigger_name         = "trigger_volleyball"
  trigger_rule         = "rate(1 minute)"
  trigger_url          = "https://www.anmeldung.sport.uni-erlangen.de/hsp/sportarten/aktueller_zeitraum_0/_Volleyball.html"
  lambda_function_name = module.lambda.lambda_function_name

  depends_on = [module.lambda]
}

# module "trigger_fitness" {
#   source = "./trigger"
# 
#   trigger_name         = "trigger_fitness"
#   trigger_rule         = "rate(2 hours)"
#   trigger_url          = "https://www.anmeldung.sport.uni-erlangen.de/hsp/sportarten/aktueller_zeitraum_0/_Fitnessstudio___Gym.html"
#   lambda_function_name = module.lambda.lambda_function_name
# }
