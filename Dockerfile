FROM python:3.10

RUN mkdir /application

WORKDIR /Calendar_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
