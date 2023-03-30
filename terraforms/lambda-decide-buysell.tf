data "archive_file" "decide_buysell" {
  type        = "zip"
  source_dir  = "../dist/decide-buysell"
  output_path = "../dist/decide-buysell.zip"
}

resource "aws_lambda_function" "decide_buysell" {
  function_name = "${var.component}_${var.env}_decide_buysell"
  filename      = data.archive_file.decide_buysell.output_path

  runtime     = "nodejs18.x"
  memory_size = var.memory_size
  handler     = "index.handler"

  source_code_hash = data.archive_file.decide_buysell.output_base64sha256
  role             = aws_iam_role.iam_lambda_role.arn

  environment {
    variables = {
      run_env = var.env
    }
  }
}