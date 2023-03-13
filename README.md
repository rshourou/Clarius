A FastAPI CRUD App
This project is a REST_API app  with a Python FastAPI backend. It is hosted on serverless AWS infrastructure (using Lambda and DynamoDB).

Clarius API app

# API Folder
The /api folder contains the Python FastAPI code. Run this shell script to build the code into a zip (required for CDK to upload to Lambda):

# Only work on UNIX (Mac/Linux) systems!
# Go to api folder cd api and run docker commands: 
docker build -t build_lambda .

docker run --rm -v "cd:/code" build_lambda

This should generate a lambda_function.zip in api folder.

# Infrastructure Folder
go to the root directory and run
The /Clarius-Infra folder contains the CDK code to deploy all the infrastructure (Lambda function and DynamoDB table) to your AWS account, SSH into your docker container.

cd ..
docker compose up -d

docker compose run -it --rm aws-cdk /bin/bash

cd Clarius/Clarius_Infra

# You will also need to configure AWS cli inside container by running in /Clarius-Infra folder

aws configure

cdk bootstrap

cdk deploy



# Test Folder
This contains the Pytest integration tests you can use to test your endpoint directly. Don't forget to change your ENDPOINT to the one you want to use (in api_integration_test.py).

You can run the test like this (but you have to have pytest installed):

pytest

Swagger 
{your end point}/docs




