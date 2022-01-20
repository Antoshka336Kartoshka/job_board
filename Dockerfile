FROM python:3.7.4-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /job_board
COPY requirements.txt /job_board

RUN apt-get update \
    && apt-get --assume-yes install gcc python-mysqldb \
    && apt-get -y install default-libmysqlclient-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /job_board

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
