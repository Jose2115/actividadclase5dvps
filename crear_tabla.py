import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def crear_tabla():
    try:
        tabla = dynamodb.create_table(
            TableName='Base_finanzas',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        tabla.wait_until_exists()
        print("Tabla creada exitosamente")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("La tabla ya existe, continuando...")

crear_tabla()