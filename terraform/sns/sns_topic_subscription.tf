resource "aws_sns_topic_subscription" "notification_email" {
  endpoint  = var.email_address
  protocol  = "email"
  topic_arn = aws_sns_topic.notification.arn
}
