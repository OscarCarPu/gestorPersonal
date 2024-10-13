1. Upload lambdas to an S3 bucket with the path `gestorpersonal/backend/lambdas`:
   aws s3 cp backend/lambdas/*.py s3://<your-bucket-name>/gestorpersonal/backend/lambdas/*.py
2. Crear el cloudformation
  aws cloudformation create-stack --stack-name <your-stack-name> --template-body file://backend/tabla.yaml --capabilities CAPABILITY_NAMED_IAM
3. Crear la api
  aws cloudformation create-stack --stack-name <your-stack-name> --template-body file://backend/api.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=LambdaBucket,ParameterValue=<bucket-name>
4. Crear usuario del pool y conseguir token:
  - Creamos el usuario y el acceso de aplicacion manualmente
  aws cognito-idp admin-initiate-auth --user-pool-id <user_pool_id> --client-id <client_id> --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters USERNAME=<username>,PASSWORD=<password> --region <region>
  - aws cognito-idp admin-respond-to-auth-challenge --user-pool-id <user_pool_id> --client-id <client_id> --challenge-name NEW_PASSWORD_REQUIRED --session <session_token> --challenge-responses USERNAME=<username>,NEW_PASSWORD=<new_password> --region <region>