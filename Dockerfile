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

# Install pip modules
#10
COPY requirements.txt .

#11
RUN pip install --upgrade pip
#12
#RUN python -m pip install --no-cache-dir --quiet -r requirements.txt
#RUN pip install --no-cache-dir --quiet -r requirements.txt
RUN pip install --upgrade build

#13
COPY . .

#14
RUN python -m build

#15
RUN pylint **/*.py
#16
RUN coverage run -m unittest tests/*_test.py
#17
RUN coverage report

#18
RUN python -m pip install .

#19
ENTRYPOINT python -m unittest tests/*_test.py
