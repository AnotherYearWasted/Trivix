FROM python:3.10.0a6-alpine3.13

WORKDIR /Trivix

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]