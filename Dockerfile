FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN mkdir -p /app/staticfiles && \
    python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "test_stripe.wsgi:application"]