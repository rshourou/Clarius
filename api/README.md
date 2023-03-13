docker build -t build_lambda .
docker run --rm -v "cd:/code" build_lambda

This should generate a lambda_function.zip in api folder.