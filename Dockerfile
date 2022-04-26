FROM python:3.10-slim-buster

RUN mkdir /chineseproverbs
COPY requirements.txt /chineseproverbs
WORKDIR /chineseproverbs
RUN pip install -r requirements.txt

COPY . /chineseproverbs

CMD ["gunicorn", "wsgi:app", "-w 2", "-b 0.0.0.8:80"]