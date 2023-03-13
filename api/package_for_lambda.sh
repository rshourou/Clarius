#!/bin/bash

# Exit if any command fails
set -eux pipefail

python3.8 -m pip install -t lambda_function -r requirements.txt
(cd lambda_function; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u main.py
#aws lambda update-function-code --function-name Clarius --zip-file fileb://lambda_function.zip

# Clean up
rm -rf lambda_function