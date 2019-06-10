# use go to get and build a static binary of tfjson
FROM golang:1 as tfjson
RUN go get github.com/wybczu/tfjson
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' github.com/wybczu/tfjson

## build our app in python
FROM python:3-slim

RUN apt-get update && apt-get install -y git

COPY --from=tfjson /go/tfjson /usr/local/bin
COPY --from=hashicorp/terraform:0.11.14 /bin/terraform /usr/local/bin

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pylint **/*.py \
    && coverage run -m unittest tests/*_test.py \
    && coverage report

RUN pip install .

ENTRYPOINT python -m unittest tests/*_test.py
