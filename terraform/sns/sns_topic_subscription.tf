resource "aws_sns_topic_subscription" "notification_email" {
  for_each  = toset(var.email_addresses)
  endpoint  = each.key
  protocol  = "email"
  topic_arn = aws_sns_topic.notification.arn
}
