import boto3

profile = 'inawisdom-auth'
region = 'us-east-1'

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

qs_user_list = qs_client.list_users(
    AwsAccountId='443607859390',
    Namespace='default'
)

print(qs_user_list)
