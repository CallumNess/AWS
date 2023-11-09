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
resource "aws_s3_bucket" "csvprocessing" {
  bucket = "csvprocessing"

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
