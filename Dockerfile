## build our app in python
FROM python:3.8-alpine3.18

RUN apk update
RUN apk upgrade
RUN apk add --no-cache --virtual .run-deps \
       python3 \
       py3-pip

RUN apk update
RUN apk upgrade
RUN rm -rf /var/cache/apk /root/.cache


COPY --from=hashicorp/terraform:latest /bin/terraform /usr/local/bin

WORKDIR /app

# Install pip modules
COPY requirements.txt .

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir --quiet -r requirements.txt

COPY . .

RUN pylint **/*.py \
RUN coverage run -m unittest tests/*_test.py \
RUN coverage report

RUN python -m pip install .

ENTRYPOINT python -m unittest tests/*_test.py
