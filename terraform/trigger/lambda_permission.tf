resource "aws_lambda_permission" "event_rule_permission" {
  statement_id  = "AllowEventRuleToInvokeLambda-${var.trigger_name}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.scheduled_trigger.arn
}
