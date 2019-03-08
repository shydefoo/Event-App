FROM python:3

WORKDIR /app
COPY src /app/src
COPY wait-for-it.sh /app
COPY requirements.txt /app

RUN mkdir /app/Images
RUN pip install -r requirements.txt
RUN chmod 777 wait-for-it.sh

ENV PYTHONPATH "${PYTHONPATH}:src"

#CMD python src/manage.py makemigrations && \
#    python src/manage.py migrate && \
#    python src/manage.py runserver 0.0.0.0:8000

CMD ./wait-for-it.sh db_service:3306 -- python django-backend/manage.py makemigrations && python django-backend/manage.py migrate && gunicorn project.wsgi -b 0.0.0.0:8000
