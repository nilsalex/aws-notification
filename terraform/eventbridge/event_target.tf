resource "aws_cloudwatch_event_target" "lambda_invocation" {
  arn  = data.aws_lambda_function.lambda_function.arn
  rule = aws_cloudwatch_event_rule.scheduled_trigger.id
}
