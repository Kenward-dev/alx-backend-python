FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "-p", "8000", "messaging_app.wsgi:application"]