FROM python:3.10-slim

WORKDIR /Calendar
COPY app/ /Calendar/app/
COPY requirements.txt /Calendar
RUN ls -la /Calendar

RUN python3 --version
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /Calendar/requirements.txt
RUN pip3 list --format=columns

ENV PYTHONPATH=.

CMD ["python", "/Calendar/app/main.py"]