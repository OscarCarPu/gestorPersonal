@echo off

:: Variables
set S3_BUCKET_NAME=oscarcarballopuebla

:: Zip the lambda function
powershell Compress-Archive -Path backend/index.py -DestinationPath backend/index.zip

:: Upload to S3
aws s3 cp backend/index.zip s3://%S3_BUCKET_NAME%/gestorpersonal/backend/index.zip

:: Delete the zip file after upload using PowerShell
powershell Remove-Item -Path backend/index.zip