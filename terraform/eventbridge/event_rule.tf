resource "aws_cloudwatch_event_rule" "scheduled_trigger" {
  name                = "scheduled-every-minute"
  schedule_expression = "rate(1 minute)"
}
