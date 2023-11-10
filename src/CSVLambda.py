import json
import boto3
import csv
import os

profile = 'inawisdom-sandbox-new-admin'
region = 'eu-west-3'

session = boto3.Session(profile_name=profile, region_name=region)

s3 = session.client('s3')
dynamodb = session.client('dynamodb')
sts = session.client('sts')
ssm = session.client('ssm')

parameter = ssm.get_parameter(Name=os.environ['DYNAMODB_NAME'])


def bucket_file(bucket):
    bucket = s3.get_object(
        Bucket='csvprocessing',
        Key='rider_details.csv',
    )


def read_csv_csv(reader):
    with open('src/rider_details.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows = row['Name']
            print(rows)


def dynamo_put(response):
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


def dynamo_put_multiple(rows):
    with open('src/rider_details.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row1 = row['Name']
            # row2 = row['Brand']
            print(f'{row1}')

    response = dynamodb.batch_write_item(
        RequestItems={
            'CSV_File_DB': [
                {
                    'PutRequest': {
                        'Item': {
                            'CSV': {
                                'S': row1[0:1],
                            },
                            'FileName': {
                                'S': row1[:-1],
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
