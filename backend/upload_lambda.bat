@echo off

:: Check if the index file name is provided
if "%1"=="" (
    echo Usage: %0 index_file_name
    exit /b 1
)

:: Variables
set S3_BUCKET_NAME=oscarcarballopuebla
set INDEX_FILE_NAME=%1

:: Zip the lambda function
powershell Compress-Archive -Path backend/%INDEX_FILE_NAME%.py -DestinationPath backend/%INDEX_FILE_NAME%.zip

:: Upload to S3
aws s3 cp backend/%INDEX_FILE_NAME%.zip s3://%S3_BUCKET_NAME%/gestorpersonal/backend/%INDEX_FILE_NAME%.zip

:: Delete the zip file after upload using PowerShell
powershell Remove-Item -Path backend/%INDEX_FILE_NAME%.zip