import boto3

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('GestorPersonal')

def handler(event, context):
  event,id = event['pathParameters']['id'].split('/')
  function_name = 'delete_' + event
  try:
    response=globals()[function_name](id)
    return {
      'statusCode': 200,
      'body': str(response)
    }
  except Exception as e:
    return {
      'statusCode': 400,
      'body': str(e)
    }

#region Gestor de Proyectos
def delete_proyecto(id):
  pass

def delete_tiempo_dedicado(id):
  pass

def delete_tarea(id):
  pass

def delete_recado(id):
  pass
#endregion
#region Horario y Calendario
def delete_evento(id):
  pass

def delete_horario(id):
  pass
#endregion

#region Finanzas

def delete_cuenta(id):
  pass

def delete_tipo_movimiento(id):
  pass

def delete_ingreso(id):
  pass

def delete_gasto(id):
  pass

def delete_transferencia(id):
  pass

def delete_presupuesto(id):
  pass

#endregion