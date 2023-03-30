resource "aws_cloudwatch_log_group" "decide_buysell" {
  name = "/aws/lambda/${aws_lambda_function.decide_buysell.function_name}"

  retention_in_days = 14
}
