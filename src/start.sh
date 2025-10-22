#!/bin/sh
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  # if run locally, run the client through emulator and pass the parameter with lambda function
  exec ./aws-lambda-rie python -m awslambdaric "$@"
else
  # if run on the cloud, run the client directly and pass the parameter with lambda function
  exec python -m awslambdaric "$@"
fi