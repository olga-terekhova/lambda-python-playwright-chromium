# Use Ubuntu as a base image
FROM ubuntu:24.04 AS builder

# Set local directory that contains lambda code, pip requirements, 
# and testing libraries (the aws lambda emulator and a script to handle testing in local vs cloud env)
ARG FUNCTION_SRC="/src"

# Set directory on the image for code, requirements, testing libraries
ARG FUNCTION_DIR="/project/function"

# Copy code, requirements, testing libraries onto the image
COPY ${FUNCTION_SRC} ${FUNCTION_DIR}

# Set directory on the image to contain Python virtual environment
ARG VIRTUAL_PATH="/project/venv"

# Set PIP to use no cache to control image size
ENV PIP_NO_CACHE_DIR=1

# Install python, create python virtual environment, install libraries (boto3, playwright, aws lambda runtime client)
# Install chromium headless and needed dependencies
RUN DEBIAN_FRONTEND=noninteractive TZ=UTC \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        tzdata python3 python3-pip python3-venv && \
    python3 -m venv ${VIRTUAL_PATH} && \
    . ${VIRTUAL_PATH}/bin/activate && \
    pip install -r ${FUNCTION_DIR}/requirements.txt && \
    playwright install chromium --only-shell && \
    playwright install-deps && \
    apt-get clean && rm -rf /var/lib/apt/lists/* 


# Activate Python virtual environment
ENV VIRTUAL_ENV=${VIRTUAL_PATH}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set working directory
WORKDIR ${FUNCTION_DIR}

# Define entrypoint as the script that runs the aws lambda runtime client 
# either directly (on cloud) or through the aws lambda emulator (locally)
ENTRYPOINT [ "./start.sh" ]

# Pass the lambda module and handler function as a parameter into the lambda runtime client
CMD ["lambda_function.handler"]