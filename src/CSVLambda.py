import boto3
# import boto3.session
import pandas
import csv

profile = 'inawisdom-sandbox-new-admin'
region = 'eu-west-3'

session = boto3.Session(profile_name=profile, region_name=region)

s3 = session.client('s3')
dynamodb = session.client('dynamodb')
sts = session.client('sts')


def bucket_file(bucket):
    bucket = s3.get_object(
        Bucket='csvprocessing',
        Key='rider_details.csv',
    )
    print(bucket)

# def read_csv_pandas():
#     file = pandas.read_csv('src/rider_details.csv')
#     print(file)


def read_csv_csv(row_index1):
    with open('src/rider_details.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row1 = [row['Name']]
            row_index1 = row1[0:1]


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


read_csv_csv('item')
