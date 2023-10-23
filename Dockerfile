FROM python:3
USER root

EXPOSE 8080:8080

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY "./requirements.txt" /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./. /app/
WORKDIR "/app"
CMD ["python","app.py"]