FROM python:3.6

WORKDIR /app

COPY polls /app
COPY requirements.txt /app/requirements.txt
COPY setup.py /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

ARG MONGO_HOST='localhost'
ARG MONGO_PORT=27017
ARG MONGO_DBNAME='kts'

RUN /bin/bash -c 'echo ${MONGO_HOST}'
RUN /bin/bash -c 'echo ${MONGO_PORT}'
RUN /bin/bash -c 'echo ${MONGO_DBNAME}'

ENV MONGO_HOST=${MONGO_HOST}
ENV MONGO_PORT=${MONGO_PORT}
ENV MONGO_DBNAME=${MONGO_DBNAME}

RUN /bin/bash -c 'echo ${MONGO_HOST}'
RUN /bin/bash -c 'echo ${MONGO_PORT}'
RUN /bin/bash -c 'echo ${MONGO_DBNAME}'

CMD ["python", "main_api_app/main.py"]