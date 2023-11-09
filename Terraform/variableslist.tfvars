s3_bucket_name       = "csvprocessing"
dynamo_db_table_name = "CSV_File_DB"
iam_role_name        = "lambda_get_object_s3_put_item_dynamodb"
iam_policy_name      = "lambda_s3_list_dynamodb_get"

# terraform apply -var-file=variableslist.tfvars (Overides the var values in the main.tf template)

# Good method of deploying dev,test,prod envs as you can create dev.tfvars, test.tfvars, prod.tfvars 
# that deploy different resouces based off variable values within each file
