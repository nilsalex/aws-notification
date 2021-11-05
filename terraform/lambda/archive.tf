data "archive_file" "lambda_function" {
  type             = "zip"
  source_file      = "${path.module}/lambda_function.py"
  output_path      = "${path.module}/lambda_function.py.zip"
  output_file_mode = "0666"
}
