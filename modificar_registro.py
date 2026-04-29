import boto3
from datetime import datetime, timezone
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('ClientesFinanzas')

def modificar_atributo(id_cliente, atributo, nuevo_valor, usuario):
    """
    Modifica un atributo y registra: qué cambió, cuándo y quién
    """
    # Obtener el elemento actual
    respuesta = tabla.get_item(Key={'id': id_cliente})
    item = respuesta.get('Item', {})

    valor_anterior = item.get(atributo, 'N/A')

    # Registro del cambio
    nuevo_cambio = {
        'atributo_modificado': atributo,
        'valor_anterior': str(valor_anterior),
        'valor_nuevo': str(nuevo_valor),
        'fecha_hora': datetime.now(timezone.utc).isoformat(),
        'usuario': usuario
    }

    historial = item.get('historial_cambios', [])
    historial.append(nuevo_cambio)

    # Actualizar en DynamoDB
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
    print(f"✅ [{usuario}] Modificó '{atributo}' de '{valor_anterior}' → '{nuevo_valor}' en {id_cliente}")

# Ejemplo de dos modificaciones registradas
modificar_atributo('CLI-0001', 'ciudad', 'Monterrey', 'jperez@finanzas.mx')
modificar_atributo('CLI-0001', 'monto_venta', 99999.99, 'mgomez@finanzas.mx')
modificar_atributo('CLI-0005', 'producto', 'Servidor', 'jperez@finanzas.mx')