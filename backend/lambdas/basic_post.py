import boto3
import json
from datetime import datetime
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, Decimal):
      return float(o)
    return super(DecimalEncoder, self).default(o)

def handler(event, context):
  body = json.loads(event['body'])
  if 'entidad' not in body:
    raise Exception('Falta la entidad')
  entidad = body['entidad']
  function_name = 'insert_' + entidad
  try:
    item=globals()[function_name](body)
    return {
      'statusCode': 200,
      'body': json.dumps(item, cls=DecimalEncoder)
    }
  except Exception as e:
    return {
      'statusCode': 400,
      'body': json.dumps(str(e))
    }
  
def get_autoincrement_id(entidad):
  table = dynamodb.Table('GestorPersonal')
  response = table.query(
    AttributesToGet=['id'],
    KeyConditions={
      'entidad': {
        'AttributeValueList': [entidad],
        'ComparisonOperator': 'EQ'
      }
    },
    ScanIndexForward=False,
    Limit=1,
    ConsistentRead=True
  )

  items = response.get('Items', [])
  if len(items) == 0:
    return 1
  else:
    return int(items[0]['id'] + 1)

def insert_proyecto(body):
  tabla = dynamodb.Table('GestorPersonal')
  default_attributes = {
    'datetime_creacion': datetime.now().isoformat(),
    'minutos_dedicados': 0,
    'estado': 'nuevo',
    'etiquetas': [],
    'descripcion': '',
  }
  obligatory_attributes = ['nombre']
  allowed_values = {
    'estado': ['nuevo', 'en curso','en pausa', 'en espera', 'cerrado']
  }
  for attr in obligatory_attributes:
    if attr not in body:
      raise Exception('Falta el atributo ' + attr)
    
  for key, value in default_attributes.items():
    if key not in body:
      body[key] = value

  for key, values in allowed_values.items():
    if key in body and body[key] not in values:
      raise Exception('Valor no permitido para ' + key)

  body['id'] = get_autoincrement_id('proyecto')
  tabla.put_item(Item=body)
  return body

def insert_tarea(body):
  tabla = dynamodb.Table('GestorPersonal')
  obligatory_attributes = ['nombre', 'proyecto_id']
  default_attributes = {
    'padre_id': None,
    'minutos_estimados': None,
    'minutos_dedicados': 0,
    'minutos_dedicados_total': 0,
    'prioridad': 0,
    'datetime_creacion': datetime.now().isoformat(),
    'datetime_fecha_limite': None,
    'estado': 'nuevo',
    'descripcion': '',
  }
  allowed_values = {
    'estado': ['nuevo', 'en curso', 'en pausa', 'en espera', 'cerrado'],
    'prioridad': [0, 1, 2, 3, 4, 5]
  }
  check_values = {
    'proyecto_id': 'proyecto',
    'padre_id': 'tarea'
  }
  for attr in obligatory_attributes:
    if attr not in body:
      raise Exception('Falta el atributo ' + attr)
    
  for key, value in default_attributes.items():
    if key not in body:
      body[key] = value

  for key, values in allowed_values.items():
    if key in body and body[key] not in values:
      raise Exception('Valor no permitido para ' + key)
    
  for key, value in check_values.items():
    if key in body:
      response = tabla.query(
        AttributesToGet=['id'],
        KeyConditions={
          'entidad': {
            'AttributeValueList': [value],
            'ComparisonOperator': 'EQ'
          },
          'id': {
            'AttributeValueList': [body[key]],
            'ComparisonOperator': 'EQ'
          }
        },
        Limit=1,
      )
      items = response.get('Items', [])
      if len(items) == 0:
        raise Exception('No existe el ' + value + ' con id ' + str(body[key]))
      
  body['id'] = get_autoincrement_id('tarea')
  tabla.put_item(Item=body)
  return body