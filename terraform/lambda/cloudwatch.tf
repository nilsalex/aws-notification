resource "aws_cloudwatch_log_group" "notification_lambda" {
  name              = "/aws/lambda/${aws_lambda_function.notification_lambda.function_name}"
  retention_in_days = 7
}