import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def crear_tabla():
    tabla = dynamodb.create_table(
        TableName='BaseFinanzas',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    tabla.wait_until_exists()
    print("✅ Tabla creada exitosamente")
    return tabla

crear_tabla()