import boto3
import random
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('Base_finanzas')

nombres = ["Carlos López", "María García", "Juan Pérez", "Ana Torres",
           "Luis Ramírez", "Sofía Martínez", "Pedro Sánchez", "Elena Díaz",
           "Miguel Flores", "Laura Hernández"]

ciudades = ["CDMX", "Guadalajara", "Monterrey", "Puebla", "Tijuana",
            "Mérida", "León", "Querétaro", "Cancún", "Toluca"]

productos = ["Laptop", "Monitor", "Teclado", "Mouse", "Impresora",
             "Teléfono", "Tablet", "Audífonos", "Cámara", "Proyector"]

with tabla.batch_writer() as batch:
    for i in range(1, 51):
        batch.put_item(Item={
            'id': f'CLI-{i:04d}',                          
            'nombre': random.choice(nombres),               
            'ciudad': random.choice(ciudades),              
            'producto': random.choice(productos),           
            'monto_venta': round(random.uniform(500, 50000), 2),  
            'fecha_registro': datetime.now(timezone.utc).isoformat(),
            'modificado_por': 'sistema',
            'historial_cambios': []
        })

print("✅ 50 registros insertados correctamente")