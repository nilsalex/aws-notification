data "aws_iam_policy_document" "lambda_execution_role_assume_role_policy" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "LambdaExecutionRole"

  assume_role_policy = data.aws_iam_policy_document.lambda_execution_role_assume_role_policy.json
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["${aws_cloudwatch_log_group.notification_lambda.arn}:*"]
    condition {
      test     = "ArnEquals"
      variable = "lambda:SourceFunctionArn"
      values   = [aws_lambda_function.notification_lambda.arn]
    }
  }
  statement {
    actions   = ["sns:Publish"]
    resources = [var.sns_topic_arn]
    condition {
      test     = "ArnEquals"
      variable = "lambda:SourceFunctionArn"
      values   = [aws_lambda_function.notification_lambda.arn]
    }
  }
  statement {
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem"]
    resources = [var.dynamodb_table_arn]
    condition {
      test     = "ArnEquals"
      variable = "lambda:SourceFunctionArn"
      values   = [aws_lambda_function.notification_lambda.arn]
    }
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name   = "NotificationLambdaPolicy"
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
