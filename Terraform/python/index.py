import json
import boto3
import csv
import os


def lambda_handler(event, context):

    # profile = '***'
    # region = 'eu-west-3'

    # session = boto3.Session(profile_name=profile, region_name=region)

    s3 = session.client('s3')
    dynamodb = session.client('dynamodb')
    sts = session.client('sts')
    ssm = session.client('ssm')

    parameter = ssm.get_parameter(Name=os.environ['DYNAMODB_NAME'])

    PATH_IN_COMPUTER = '/Users/callumness/Documents/Python Personal/Github/AWS/src/rider_details.csv'

    s3.put_object(
        Bucket='csvprocessing',
        Key='rider_details.csv',
        Body=open(PATH_IN_COMPUTER, 'rb')
    )

    s3.get_object(
        Bucket='csvprocessing',
        Key='rider_details.csv',
    )

    # with open('src/rider_details.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         rows = row['Name']
    #         print(rows)

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

    with open('src/rider_details.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row1 = row['Name']
            # row2 = row['Brand']

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
