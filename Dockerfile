## build our app in python
#1
FROM python:3.8-alpine3.18

#2
RUN apk update
#3
RUN apk upgrade
#4
RUN apk add --no-cache --virtual .run-deps \
       python3 \
       py3-pip

#5
RUN apk update
#6
RUN apk upgrade
#7
RUN rm -rf /var/cache/apk /root/.cache

#8
COPY --from=hashicorp/terraform:latest /bin/terraform /usr/local/bin

#9
WORKDIR /app

# Install pip modules
#10
COPY requirements.txt .

#11
RUN pip install --upgrade pip
#12
RUN python -m pip install --no-cache-dir --quiet -r requirements.txt

#13
COPY . .

#14
RUN pylint **/*.py \
#15
RUN coverage run -m unittest tests/*_test.py \
#16
RUN coverage report

#17
RUN python -m pip install .

#18
ENTRYPOINT python -m unittest tests/*_test.py
