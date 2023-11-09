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
        Action   = ["dynamodb:putitem"]
        Effect   = "Allow"
        Resource = [aws_dynamodb_table.dynamodb-table.arn]
      },
      {
        Action   = ["ssm:Get*"]
        Effect   = "Allow"
        Resource = [aws_ssm_parameter.dynamodb.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policies" {
  role       = aws_iam_role.lambda_s3_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
