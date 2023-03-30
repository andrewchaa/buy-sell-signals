data "aws_iam_policy_document" "iam_lambda_log_policy_document" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "${aws_cloudwatch_log_group.decide_buysell.arn}:*"
    ]
  }
}

resource "aws_iam_policy" "iam_lambda_log_policy" {
  name   = "${var.component}_${var.env}_iam_lambda_log_policy"
  policy = data.aws_iam_policy_document.iam_lambda_log_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_lambda_role.name
  policy_arn = aws_iam_policy.iam_lambda_log_policy.arn
}
