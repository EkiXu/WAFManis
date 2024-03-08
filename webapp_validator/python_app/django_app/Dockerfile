FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app

EXPOSE 6000
CMD ["python","manage.py","runserver","0.0.0.0:6000"]
