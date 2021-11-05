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
  }
}
