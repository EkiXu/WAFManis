FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY app.py /app/

EXPOSE 8080
CMD ["python","app.py"]
