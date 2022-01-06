FROM python:3.7.4
ENV PYTHONUNBUFFERED=1

WORKDIR /job_board
COPY requirements.txt /job_board

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /job_board

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
