import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

BUCKET_NAME = 'finanzas-mexico-datos'  # Cambia por tu bucket

def exportar_a_s3():
    tabla = dynamodb.Table('Base_Finanzas')
    respuesta = tabla.scan()
    items = respuesta['Items']

    # Generar contenido del .txt
    lineas = []
    lineas.append("=" * 70)
    lineas.append(f"REPORTE FINANZAS MÉXICO - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    lineas.append("=" * 70)

    for item in sorted(items, key=lambda x: x['id']):
        lineas.append(f"\n🔹 ID: {item['id']}")
        lineas.append(f"   Nombre:   {item.get('nombre', 'N/A')}")
        lineas.append(f"   Ciudad:   {item.get('ciudad', 'N/A')}")
        lineas.append(f"   Producto: {item.get('producto', 'N/A')}")
        lineas.append(f"   Monto:    ${item.get('monto_venta', 0):,.2f}")
        lineas.append(f"   Modificado por: {item.get('modificado_por', 'sistema')}")

        historial = item.get('historial_cambios', [])
        if historial:
            lineas.append(f"   📋 Historial de cambios ({len(historial)}):")
            for cambio in historial:
                lineas.append(f"      [{cambio['fecha_hora']}] {cambio['usuario']}")
                lineas.append(f"      {cambio['atributo_modificado']}: '{cambio['valor_anterior']}' → '{cambio['valor_nuevo']}'")

    contenido = "\n".join(lineas)

    # Subir a S3
    nombre_archivo = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=nombre_archivo,
        Body=contenido.encode('utf-8'),
        ContentType='text/plain'
    )
    print(f"✅ Archivo '{nombre_archivo}' subido a S3 exitosamente")

exportar_a_s3()