1. Subir lambda.py a un s3 bucket con la dirección gestorpersonal/backend/lambda.py:
  aws s3 cp backend/lambda.py s3://your-bucket-name/gestorpersonal/backend/lambda.py
2. Crear el cloudformation
  aws cloudformation create-stack --stack-name your-stack-name --template-body file://backend/tabla.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=S3BucketName,ParameterValue=your-bucket-name
 