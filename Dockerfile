FROM python:3.9

WORKDIR /app

COPY ./functions /app/functions
COPY requirements.txt .

RUN pip install -r "requirements.txt"

CMD ["python", "functions/main.py"]