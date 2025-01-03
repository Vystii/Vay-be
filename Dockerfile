FROM python:3.11

WORKDIR /app

COPY VayBe/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY VayBe .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
