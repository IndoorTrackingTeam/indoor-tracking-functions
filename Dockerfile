FROM python:3.9

WORKDIR /app

COPY ./functions ./functions
COPY requirements.txt .

RUN pip install -r "requirements.txt"

WORKDIR /app/functions
CMD ["python", "main.py"]