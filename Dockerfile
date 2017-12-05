FROM python:2.7.10

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src/ /app

EXPOSE 8000

CMD python manage.py runserver
