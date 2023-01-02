FROM python:3.8-buster

WORKDIR /workdir
ENV PYTHONPATH "${PYTHONPATH}:/workdir/app"

COPY requirements.txt .
COPY app ./app
RUN pip install -r requirements.txt

COPY .env .
COPY alembic.ini .
COPY migrations ./migrations
COPY gunicorn.conf.py .


EXPOSE 8080
CMD ["gunicorn", "--config", "./gunicorn.conf.py", "app.main:app"]