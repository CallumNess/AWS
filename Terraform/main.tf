# Improvement comments

# move providers into a providers.tf file

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.24.0"
    }
  }
}
provider "aws" {
  profile = "inawisdom-sandbox-new-admin"
  region  = "eu-west-3"
}

data "archive_file" "python_function" {
  type        = "zip"
  source_dir  = "${path.module}/python/"
  output_path = "${path.module}/python/python-lambda.zip"
}

#Update resources to Input Variables for reuseability. 


resource "aws_s3_bucket" "csvprocessing" {
  bucket = "csvprocessing"
  # bucket = var.s3_bucket_name (example of variable usage)

  tags = {
    Name = "Bucket for CSV file processing"
  }
}


resource "aws_dynamodb_table" "dynamodb-table" {
  name           = "CSV_File_DB"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "CSV"
  range_key      = "FileName"

  attribute {
    name = "CSV"
    type = "S"
  }

  attribute {
    name = "FileName"
    type = "S"
  }
  tags = {
    Name = "CSV File DB"
  }
}


resource "aws_ssm_parameter" "dynamodb" {
  name  = "Dynamodb_param"
  type  = "String"
  value = "CSV_File_DB"
}

resource "aws_iam_role" "lambda_s3_role" {
  name = "lambda_get_object_s3_put_item_dynamodb"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_s3_list_dynamodb_get"
  description = "Lambda policy for S3 List and DynamoDB Get"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:ListBucket"]
        Effect   = "Allow"
        Resource = [aws_s3_bucket.csvprocessing.arn]
      },
      {
        Action   = ["s3:GetObject"]
        Effect   = "Allow"
        Resource = ["${aws_s3_bucket.csvprocessing.arn}/*"]
      },
      {
        Action   = ["dynamodb:putitem", "dynamodb:BatchWriteItem"]
        Effect   = "Allow"
        Resource = [aws_dynamodb_table.dynamodb-table.arn]
      },
      {
        Action   = ["ssm:GetParameter"]
        Effect   = "Allow"
        Resource = [aws_ssm_parameter.dynamodb.arn]
      },
      {
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:CreateLogGroup"],
        Effect   = "Allow"
        Resource = [aws_cloudwatch_log_group.lambda_logs.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policies" {
  role       = aws_iam_role.lambda_s3_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/CSV_Processor_Lambda"
}

resource "aws_lambda_function" "terraform_lambda_func" {
  filename      = "${path.module}/python/python-lambda.zip"
  function_name = "CSV_Processor_Lambda"
  role          = aws_iam_role.lambda_s3_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.11"
  depends_on    = [aws_iam_role_policy_attachment.attach_policies]
  timeout       = 10
  environment {
    variables = {
      SSMParameterName = aws_ssm_parameter.dynamodb.name
    }
  }
}
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.csvprocessing.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.terraform_lambda_func.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "s3_allow_lambda_exec" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.terraform_lambda_func.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.csvprocessing.arn
}
