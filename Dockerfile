## build our app in python
#1
FROM alpine

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
#10
ENV PYTHONPATH /app/aws_terraform_test_runner

# Install pip modules
#11
COPY requirements.txt .

#12
RUN pip install --upgrade pip
#13
#RUN python -m pip install --no-cache-dir --quiet -r requirements.txt
RUN pip install --no-cache-dir --quiet -r requirements.txt
#14
RUN pip install --upgrade build

#15
COPY . .

#16
RUN python -m build

#17
RUN pylint **/*.py
#18
RUN coverage run -m unittest tests/*_test.py
#19
RUN coverage report

#20
RUN python -m pip install .

#21
ENTRYPOINT python -m unittest tests/*_test.py
