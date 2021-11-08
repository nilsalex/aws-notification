resource "aws_cloudwatch_event_rule" "scheduled_trigger" {
  name                = var.trigger_name
  schedule_expression = var.trigger_rule
}
