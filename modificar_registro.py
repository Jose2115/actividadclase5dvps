import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('Base_finanzas')  # nombre exacto con f minúscula

def modificar_atributo(id_cliente, atributo, nuevo_valor, usuario):
    respuesta = tabla.get_item(Key={'id': id_cliente})
    item = respuesta.get('Item', {})

    if not item:
        print(f"⚠️ ID {id_cliente} no encontrado, saltando...")
        return

    valor_anterior = item.get(atributo, 'N/A')

    nuevo_cambio = {
        'atributo_modificado': atributo,
        'valor_anterior': str(valor_anterior),
        'valor_nuevo': str(nuevo_valor),
        'fecha_hora': datetime.now(timezone.utc).isoformat(),
        'usuario': usuario
    }

    historial = item.get('historial_cambios', [])
    historial.append(nuevo_cambio)

    tabla.update_item(
        Key={'id': id_cliente},
        UpdateExpression="""
            SET #attr = :nuevo_valor,
                modificado_por = :usuario,
                ultima_modificacion = :fecha,
                historial_cambios = :historial
        """,
        ExpressionAttributeNames={'#attr': atributo},
        ExpressionAttributeValues={
            ':nuevo_valor': nuevo_valor,
            ':usuario': usuario,
            ':fecha': datetime.now(timezone.utc).isoformat(),
            ':historial': historial
        }
    )
    print(f"✅ [{usuario}] Modificó '{atributo}': '{valor_anterior}' → '{nuevo_valor}'")

# Obtener IDs reales de la tabla
print("Obteniendo items de la tabla...")
response = tabla.scan(Limit=5)
items = response.get('Items', [])

if len(items) < 2:
    print("❌ No hay suficientes items en la tabla")
    exit(1)

# Modificar con IDs reales
id1 = items[0]['id']
id2 = items[1]['id']

modificar_atributo(id1, 'ciudad', 'Monterrey', 'jperez@finanzas.mx')
modificar_atributo(id1, 'monto_venta', '99999.99', 'mgomez@finanzas.mx')
modificar_atributo(id2, 'producto', 'Servidor', 'jperez@finanzas.mx')

print("✅ Modificaciones registradas exitosamente")