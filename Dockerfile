# Terraform version passed in from Drone
ARG TERRAFORM_VERSION=${TERRAFORM_VERSION}

# Will COPY terrafrom exe FROM this source image
FROM hashicorp/terraform:${TERRAFORM_VERSION} as source_image

# Base our Docker image on the latest Alpine Linux image
FROM alpine

# Add the lastest Python3 & Pip
RUN apk add --update --upgrade --no-cache --virtual .run-deps \
    python3 \
    py3-pip \
    git \
    openssh
RUN rm -rf /var/cache/apk /root/.cache

# Get the latest terraform binary
COPY --from=source_image /bin/terraform /usr/local/bin

WORKDIR /app

# Let Python know where to find the aws_terraform_test_runner module
ENV PYTHONPATH /app/aws_terraform_test_runner

# Install pip modules
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --quiet -r requirements.txt
RUN pip install --upgrade build

COPY . .

# Build the aws_terraform_test_runner module
RUN python -m build

# Check it's all good
RUN pylint **/*.py
RUN coverage run -m unittest tests/*_test.py
RUN coverage report

# Install the aws_terraform_test_runner module
RUN python -m pip install .

# When this Docker Image is called, run this command to unit-test the python tests
ENTRYPOINT python -m unittest tests/*_test.py
