terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "1.5.7"
    }
  }
}
provider "aws" {
  profile = "inawisdom-auth"
  region  = "eu-west-1"
}
resource "aws_s3_bucket" "CSV Processing" {
  bucket = "CSV-Processing"

  tags = {
    Name = "Bucket for CSV file processing"
  }
}
resource "aws_iam_role" "lambda_role" {
  name = "CSV_File_Processing_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "CSV_File_Processing_policy"
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Action = ["s3:ListBucket"],
          Effect = "Allow",
          Resource = "${aws_s3_bucket.CSV-Processing.arn}"
        }
      ]
    })
  }

  inline_policy {
    name = "DynamoDB_Write_access"
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Action = ["dynamodb:UpdateItem"],
          Effect = "Allow",
          Resource = "${aws_dynamodb_table.CSV_File_DB.arn}"
        }
      ]
    })
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
