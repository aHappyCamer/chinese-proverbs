FROM python:3.10-slim-buster

RUN mkdir /chineseproverbs
COPY requirements.txt /chineseproverbs
WORKDIR /chineseproverbs
RUN pip install -r requirements.txt

COPY . /chineseproverbs

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]