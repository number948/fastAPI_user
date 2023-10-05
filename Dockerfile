FROM python:3.11.1-slim

RUN apt-get update && apt-get install -y libmagic1

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY app /code/app
COPY migrations /code/migrations
COPY alembic.ini requirements.txt /code/

RUN pip install --no-cache-dir -r /code/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]