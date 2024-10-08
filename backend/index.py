import boto3
from datetime import datetime
import logging

dynamodb = boto3.resource('dynamodb')
logging.basicConfig(level=logging.INFO)


def handler(event, context):
  for record in event['Records']:
    tipo_evento = record['eventName']
    if tipo_evento == 'INSERT':
      nuevo_registro = record['dynamodb']['NewImage']
      entidad = nuevo_registro['entidad']['S']
      function_name = 'insert_' + entidad
      if function_name in globals():
        try:
          globals()[function_name](nuevo_registro)
        except Exception as e:
          logging.error(f"Error in {function_name}: {e}")
      else:
        logging.error(f"Function {function_name} not found.")
    elif tipo_evento == 'MODIFY':
      nuevo_registro = record['dynamodb']['NewImage']
      viejo_registro = record['dynamodb']['OldImage']
      entidad = nuevo_registro['entidad']['S']
      function_name = 'modify_' + entidad
      if function_name in globals():
        try:
          globals()[function_name](nuevo_registro, viejo_registro)
        except Exception as e:
          logging.error(f"Error in {function_name}: {e}")
      else:
        logging.error(f"Function {function_name} not found.")
    elif tipo_evento == 'REMOVE':
      viejo_registro = record['dynamodb']['OldImage']
      entidad = viejo_registro['entidad']['S']
      function_name = 'delete_' + entidad
      if function_name in globals():
        try:
          globals()[function_name](viejo_registro)
        except Exception as e:
          logging.error(f"Error in {function_name}: {e}")
      else:
        logging.error(f"Function {function_name} not found.")

def get_autoincrement_id(nombre_entidad):
  tabla = dynamodb.Table('GestorPersonal')
  response = tabla.query(
    KeyConditionExpression=boto3.dynamodb.conditions.Key('entidad').eq(nombre_entidad),
    ScanIndexForward=False,
    Limit=1
  )

  items = response.get('Items', [])
  if not items:
    return 1
  return items[0]['id'] + 1

def insert_proyecto(objeto):
  logging.info("insert_proyecto called with objeto: %s", objeto)
  attributos_defecto = {
    'datetime_creacion': datetime.now().isoformat(),
    'minutos_dedicados': 0,
    'estado': 'nuevo',
    'etiquetas': [],
    'descripcion': ''
  }
  attributos_obligatorio = ['nombre']
  for key in attributos_obligatorio:
    if key not in objeto:
      raise Exception('El atributo {} es obligatorio'.format(key))
      return
  id = get_autoincrement_id('proyecto')
  objeto['id'] = id
  for key in attributos_defecto:
    if key not in objeto:
      objeto[key] = attributos_defecto[key]
  tabla = dynamodb.Table('GestorPersonal')
  tabla.put_item(Item=objeto)