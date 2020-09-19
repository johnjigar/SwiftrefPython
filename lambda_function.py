from dynamodb_load_data import *
from dynamodb_tables import *


def lambda_handler(event, context):
    print('In lambda_handler')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    process_data(bucket_name, key)

#create_tables()
#process_data('swiftrefacg1', 'ACCOUNTNBFORMAT_V1_MONTHLY_FULL_20200327.txt')


