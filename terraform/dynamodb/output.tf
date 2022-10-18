output "dynamodb_table_arn" {
  value = aws_dynamodb_table.lambda_state_table.arn
}