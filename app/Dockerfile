FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /Calendar
COPY ./app ./app
COPY ./requirements.txt /Calendar
RUN ls -la /Calendar

RUN python3 --version
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /Calendar/requirements.txt
RUN pip3 list --format=columns

ENV PYTHONPATH=.

EXPOSE 8000

CMD ["python", "/Calendar/app/main.py"]