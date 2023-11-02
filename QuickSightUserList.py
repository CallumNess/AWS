import boto3

profile = ''
region = ''

session = boto3.Session(profile_name=profile, region_name=region)
client = boto3.client('quicksight')
qs_client = session.client('quicksight')
sts = session.client('sts')
iam = session.client('iam')


def get_account_id():
    account_id = sts.get_caller_identity().get('Account')
    return account_id


def get_account_alias():
    alias = iam.list_account_aliases()['AccountAliases'][0]
    return alias


accountId = get_account_id()
try:
    alias = get_account_alias()
except IndexError:
    alias = 'Not set'

print(f'alias is {alias}')
print(f'accountId is {accountId}')

response = qs_client.list_users(
    AwsAccountId=get_account_id(),
    Namespace='default'
)

print(response)
