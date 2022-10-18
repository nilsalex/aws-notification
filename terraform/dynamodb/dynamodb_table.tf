resource "aws_dynamodb_table" "lambda_state_table" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "Id"
    type = "S"
  }

  hash_key = "Id"
}