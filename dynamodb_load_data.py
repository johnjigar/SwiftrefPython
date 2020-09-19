import io
from dynamodb_tables import *

def process_data(bucket_name, key):
    s3client = boto3.client('s3')
    # TODO implement

    # print(event)

    try:

        file_name = 's3://' + bucket_name + '/' + key
        print(file_name)
        tableName = get_table_name(key)
        uai = 'uai20001938-'
        print('Bucket: ' + bucket_name)
        print('Key: ' + key)
        print('Table name: ' + tableName)
        # Create a file object using the bucket and object key.
        fileObject = s3client.get_object(Bucket=bucket_name, Key=key)
        # open the file object and read it into the variable filedata.
        fileData = io.BytesIO(fileObject['Body'].read())

        # file data will be a binary stream.  We have to decode it
        # print('Encoding file')
        # contents = fileData.decode('utf-8')
        # print(contents)

        print('Calling read_csv')
        items = read_csv(fileData, '\t')
        # print(items)
        print('Calling batch_write')
        batch_write(items, uai + tableName)

    except Exception as e:
        print(e)
        print('Unable to process file...\n')

#delete_tables()
#create_tables()
#process_data('swiftrefacg', 'ACCOUNTNBFORMAT_V1_MONTHLY_FULL_20200327.txt')