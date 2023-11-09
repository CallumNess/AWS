output "bucket_arn" {
  value = "${aws_s3_bucket.CSV-Processing.arn}"
}
output "dynamodb_arn" {
    value = "${aws_dynamodb_table.CSV_File_DB.arn}"
}
