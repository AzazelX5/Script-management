FROM python:2.7.10

WORKDIR /app

COPY src/ /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py runserver
