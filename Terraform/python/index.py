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

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)

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

    # response = dynamodb.batch_write_item(
    #     RequestItems={
    #         'CSV_File_DB': [
    #             {
    #                 'PutRequest': {
    #                     'Item': {
    #                         'CSV': {
    #                             'S': 'Test1',
    #                         },
    #                         'FileName': {
    #                             'S': 'Test1',
    #                         }
    #                     },
    #                 },
    #             },
    #             {
    #                 'PutRequest': {
    #                     'Item': {
    #                         'CSV': {
    #                             'S': 'Test2',
    #                         },
    #                         'FileName': {
    #                             'S': 'Test2',
    #                         }
    #                     },
    #                 },
    #             },
    #             {
    #                 'PutRequest': {
    #                     'Item': {
    #                         'CSV': {
    #                             'S': 'Test3',
    #                         },
    #                         'FileName': {
    #                             'S': 'Test3',
    #                         }
    #                     },
    #                 },
    #             },
    #         ],
    #     },
    # )
