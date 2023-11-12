import json
import boto3
import csv
import os
import io

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
ssm = boto3.client('ssm')


def lambda_handler(event, context):

    parameter = ssm.get_parameter(Name=os.environ['SSMParameterName'])

    # Get bucket name and key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get object from bucket
    response = s3.get_object(Bucket=bucket, Key=key)

    # Pull data from the CSV and assign to variable for DynamoDB data entry
    data = response['Body'].read().decode('utf-8')
    reader = csv.reader(io.StringIO(data))
    next(reader)
    for row in reader:
        print(str.format("Name - {}, Brand - {}, Random - {}",
              row[0], row[1], row[2]))

    response = dynamodb.put_item(
        TableName="CSV_File_DB",
        Item={
            'CSV': {
                'S': "CSV",
            },
            'FileName': {
                'S': key,
            },
        },
    )
