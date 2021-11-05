resource "aws_sns_topic_subscription" "notification_sms" {
  endpoint  = var.phone_number
  protocol  = "sms"
  topic_arn = aws_sns_topic.notification.arn
}
