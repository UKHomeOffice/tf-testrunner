# use go to get and build a static binary of tfjson
FROM golang:1 as tfjson
RUN go get github.com/wybczu/tfjson
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' github.com/wybczu/tfjson

## build our app in python
FROM python:3-slim

COPY --from=tfjson /go/tfjson /usr/local/bin
COPY --from=hashicorp/terraform /bin/terraform /usr/local/bin

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pylint **/*.py \
    && coverage run -m unittest tests/*_test.py \
    && coverage report

RUN pip install .

CMD python -m unittest tests/*_test.py