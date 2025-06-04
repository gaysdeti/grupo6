FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install flask

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
