import json
import boto3
import csv
import os


def lambda_handler(event, context):

    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')
    ssm = boto3.client('ssm')

    parameter = ssm.get_parameter(Name=os.environ['SSMParameterName'])

    response = dynamodb.put_item(
        TableName="CSV_File_DB",
        Item={
            'CSV': {
                'S': 'CSV',
            },
            'FileName': {
                'S': "rider_details",
            },
        },
    )

    response = dynamodb.batch_write_item(
        RequestItems={
            'CSV_File_DB': [
                {
                    'PutRequest': {
                        'Item': {
                            'CSV': {
                                'S': 'Test1',
                            },
                            'FileName': {
                                'S': 'Test1',
                            }
                        },
                    },
                },
                {
                    'PutRequest': {
                        'Item': {
                            'CSV': {
                                'S': 'Test2',
                            },
                            'FileName': {
                                'S': 'Test2',
                            }
                        },
                    },
                },
                {
                    'PutRequest': {
                        'Item': {
                            'CSV': {
                                'S': 'Test3',
                            },
                            'FileName': {
                                'S': 'Test3',
                            }
                        },
                    },
                },
            ],
        },
    )
