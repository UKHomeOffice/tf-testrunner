## build our app in python
FROM quay.io/ukhomeofficedigital/centos-base:v0.5.14.1

RUN yum update --quiet -y \
    && yum install --quiet -y \
    git \
    wget \
    make \
    gcc \
    openssl-devel \
    zlib-devel \
    pcre-devel \
    bzip2-devel \
    libffi-devel \
    epel-release \
    sqlite-devel \
    && yum clean all --quiet -y

COPY --from=hashicorp/terraform:0.12.25 /bin/terraform /usr/local/bin

WORKDIR /app

# Install Python3.7.2 and pip modules
RUN cd /usr/bin && \
    wget --quiet https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz && \
    tar xzf Python-3.7.2.tgz && \
    cd Python-3.7.2 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    alternatives --install /usr/bin/python python /usr/local/bin/python3.7 1

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --quiet -r requirements.txt

# Fix yum installer with Python3.7 running as a global default
RUN sed -i '/#!\/usr\/bin\/python/c\#!\/usr\/bin\/python2.7' /usr/bin/yum && \
    sed -i '/#! \/usr\/bin\/python/c\#! \/usr\/bin\/python2.7' /usr/libexec/urlgrabber-ext-down

COPY . .

RUN pylint **/*.py \
    && coverage run -m unittest tests/*_test.py \
    && coverage report

RUN python -m pip install .

ENTRYPOINT python -m unittest tests/*_test.py
