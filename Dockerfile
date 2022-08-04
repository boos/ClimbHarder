# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000/tcp

CMD [ "python3", "-m" , "uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=$PORT"]