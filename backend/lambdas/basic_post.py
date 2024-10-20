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

#region Gestor de Proyectos

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
    'datetime_finalizada': None,
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

def insert_recado(body):
  tabla = dynamodb.Table('GestorPersonal')
  obligatory_attributes = ['nombre','tarea_id']
  default_attributes = {
    'datetime_creacion': datetime.now().isoformat(),
    'estado': 'nuevo',
    'descripcion': '',
    'prioridad': 0,
    'datetime_finalizada': None
  }
  allowed_values = {
    'estado': ['nuevo', 'en curso', 'en pausa', 'en espera', 'cerrado'],
    'prioridad': [0, 1, 2, 3, 4, 5]
  }
  check_values = {
    'tarea_id': 'tarea'
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
        raise Exception('No existe la ' + value + ' con id ' + str(body[key]))
      
  body['id'] = get_autoincrement_id('recado')
  tabla.put_item(Item=body)
  return body

def insert_tiempo_dedicado(body):
  tabla = dynamodb.Table('GestorPersonal')
  obligatory_attributes = ['tarea_id', 'minutos']
  default_attributes = {
    'datetime': datetime.now().isoformat(),
    'descripcion': ''
  }
  check_values = {
    'tarea_id': 'tarea'
  }
  for attr in obligatory_attributes:
    if attr not in body:
      raise Exception('Falta el atributo ' + attr)
    
  for key, value in default_attributes.items():
    if key not in body:
      body[key] = value

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
        raise Exception('No existe la ' + value + ' con id ' + str(body[key]))

  actualizar_minutos_tarea(body['tarea_id'], body['minutos'])
      
  body['id'] = get_autoincrement_id('tiempo_dedicado')
  tabla.put_item(Item=body)
  return body

def actualizar_minutos_tarea(tarea_id, minutos):
  tabla = dynamodb.Table('GestorPersonal')
  response = tabla.query(
    AttributesToGet=['minutos_dedicados_total'],
    KeyConditions={
      'entidad': {
        'AttributeValueList': ['tarea'],
        'ComparisonOperator': 'EQ'
      },
      'id': {
        'AttributeValueList': [tarea_id],
        'ComparisonOperator': 'EQ'
      }
    },
    Limit=1,
  )
  items = response.get('Items', [])
  if len(items) == 0:
    raise Exception('No existe la tarea con id ' + str(tarea_id))
  padre_id = items[0]['padre_id']
  if padre_id:
    actualizar_minutos_padre(padre_id, minutos)
  else:
    proyecto_id = items[0]['proyecto_id']
    actualizar_minutos_proyecto(proyecto_id, minutos)
  tabla.update_item(
    Key={
      'entidad': 'tarea',
      'id': tarea_id
    },
    UpdateExpression='SET minutos_dedicados_total = minutos_dedicados_total + :val, minutos_dedicados = minutos_dedicados + :val',
    ExpressionAttributeValues={
      ':val': Decimal(minutos)
    }
  )

def actualizar_minutos_padre(padre_id, minutos):
  tabla = dynamodb.Table('GestorPersonal')
  response = tabla.query(
    AttributesToGet=['minutos_dedicados_total'],
    KeyConditions={
      'entidad': {
        'AttributeValueList': ['tarea'],
        'ComparisonOperator': 'EQ'
      },
      'id': {
        'AttributeValueList': [padre_id],
        'ComparisonOperator': 'EQ'
      }
    },
    Limit=1,
  )
  items = response.get('Items', [])
  if len(items) == 0:
    raise Exception('No existe la tarea con id ' + str(padre_id))
  padre_id = items[0]['padre_id']
  if padre_id:
    actualizar_minutos_padre(padre_id, minutos)
  else:
    proyecto_id = items[0]['proyecto_id']
    actualizar_minutos_proyecto(proyecto_id, minutos)
  tabla.update_item(
    Key={
      'entidad': 'tarea',
      'id': padre_id
    },
    UpdateExpression='SET minutos_dedicados_total = minutos_dedicados_total + :val',
    ExpressionAttributeValues={
      ':val': Decimal(minutos)
    }
  )

def actualizar_minutos_proyecto(proyecto_id, minutos):
  tabla = dynamodb.Table('GestorPersonal')
  tabla.update_item(
    Key={
      'entidad': 'proyecto',
      'id': proyecto_id
    },
    UpdateExpression='SET minutos_dedicados = minutos_dedicados + :val',
    ExpressionAttributeValues={
      ':val': Decimal(minutos)
    }
  )

#endregion

#region Calendario y Horario
def insert_evento(body):
  tabla = dynamodb.Table('GestorPersonal')
  obligatory_attributes = ['nombre', 'datetime_inicio', 'datetime_fin', 'tarea.id']
  default_attributes = {
    'descripcion': '',
    'datetime_creacion': datetime.now().isoformat()
  }
  check_values = {
    'tarea.id': 'tarea'
  }
  for attr in obligatory_attributes:
    if attr not in body:
      raise Exception('Falta el atributo ' + attr)
    
  for key, value in default_attributes.items():
    if key not in body:
      body[key] = value

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
        raise Exception('No existe la ' + value + ' con id ' + str(body[key]))
      
  body['id'] = get_autoincrement_id('evento')
  tabla.put_item(Item=body)
  return body

def insert_horario(body):
  tabla = dynamodb.Table('GestorPersonal')
  obligatory_attributes = ['tarea_id','time_inicio','time_fin','date_inicio','date_fin']
  default_attributes = {
    'datetime_creacion': datetime.now().isoformat(),
    'dias': []
  }
  check_values = {
    'tarea_id': 'tarea'
  }
  allowed_values = {
    'dias': [0,1,2,3,4,5,6]
  }
  for attr in obligatory_attributes:
    if attr not in body:
      raise Exception('Falta el atributo ' + attr)
    
  for key, value in default_attributes.items():
    if key not in body:
      body[key] = value

  for key, values in allowed_values.items():
    if key in body:
      for value in body[key]:
        if value not in values:
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
        raise Exception('No existe la ' + value + ' con id ' + str(body[key]))
        
  body['id'] = get_autoincrement_id('horario')
  tabla.put_item(Item=body)
  return body