## build our app in python
FROM python:3.8-alpine3.18


COPY --from=hashicorp/terraform:latest /bin/terraform /usr/local/bin

WORKDIR /app

# Install pip modules
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --quiet -r requirements.txt

RUN pylint **/*.py \
    && coverage run -m unittest tests/*_test.py \
    && coverage report

RUN python -m pip install .

ENTRYPOINT python -m unittest tests/*_test.py
