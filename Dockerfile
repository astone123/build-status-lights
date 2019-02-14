FROM python:3

ADD . .
COPY config.yaml config.yaml
RUN pip install -r requirements.txt && pip install gunicorn

EXPOSE 8000

CMD gunicorn -w 2 --log-level=debug --preload --bind 0.0.0.0:8000 server:app

