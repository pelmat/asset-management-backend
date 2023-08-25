
FROM python:3.10.9-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /srv/app
COPY requirements.txt /srv/app/
RUN pip install -r requirements.txt
COPY . /srv/app/