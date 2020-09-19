import boto3
import pandas as pd

region_name='us-east-1'
uai = 'uai20001938-'
table_acn = {'TableName': uai + 'AccountNumberFormat', 'HashKey': 'isoCountryCode', 'RCU': 1, 'WCU': 1}
table_ibans = {'TableName': uai + 'IbanStructure', 'HashKey': 'isoCountryCode', 'RCU': 1, 'WCU': 1}
table_ibanp = {'TableName': uai + 'IbanPlus', 'HashKey': 'nationalIdCountry', 'RCU': 1, 'WCU': 1}

tables = []
tables.append(table_acn)
tables.append(table_ibans)
tables.append(table_ibanp)


def create_table(tableName, hashKey, rcu, wcu):
    client = boto3.client('dynamodb', region_name)

    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': hashKey,
                'AttributeType': 'S'
            },
        ],
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': hashKey,
                'KeyType': 'HASH'
            },
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': rcu,
            'WriteCapacityUnits': wcu
        }
    )

    return response


def delete_table(tableName):
    client = boto3.client('dynamodb', region_name)

    response = ''
    try:
        response = client.delete_table(
            TableName=tableName
        )
    except Exception as e:
        response = str(e)

    return response


def delete_tables():
    for table in tables:
        # print(table['TableName'])
        response = delete_table(table['TableName'])
        print(response)


def create_tables():
    for table in tables:
        # print(table['TableName'])
        response = create_table(table['TableName'], table['HashKey'], table['RCU'], table['WCU'])
        print(response)

def batch_write(items, tableName):
    message = "Inserting data into " + tableName
    print(message)
    dynamodb = boto3.resource('dynamodb', region_name)
    table = dynamodb.Table(tableName)
    counter = 0
    with table.batch_writer() as batch:
        for item in items:
            counter = counter + 1
            try:
                print(counter)
                batch.put_item(Item=item)
            except Exception as e:
                message = e
        message = "Successfully inserted data into..." + tableName
    print(message)
    return message

def read_csv(fileData, delimiter):
    try:
        print('Readning file')
        df = pd.read_csv(fileData, delimiter, dtype=str)
        df = df.rename(columns={
            'ISO COUNTRY CODE': 'isoCountryCode'
            , 'IBAN COUNTRY CODE': 'isoCountryCode'
        })

        #df = df.assign(nationalIDCountry=df['IBAN NATIONAL ID'] + '-' + df['IBAN ISO COUNTRY CODE'])


        print('Read file')
        df.fillna(" ", inplace=True)
        dict = df.T.to_dict()
        items = dict.values()
        return items
    except Exception as e:
        print(e)
        print('Failed to read file...\n')

def get_table_name(key):
    if ('IBANSTRUCTURE' in key):
        return 'IbanStructure'
    elif ('ACCOUNTNBFORMAT' in key):
        return 'AccountNumberFormat'
    elif ('IBANPLUS' in key):
        return 'IbanPlus'
    elif ('BANKDIRECTORY' in key):
        return 'BankDirectory'
    else:
        return 'nothing'