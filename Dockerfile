FROM python:3.10-slim-buster

RUN mkdir /chinese-proverbs
COPY requirements.txt /chinese-proverbs
WORKDIR /chinese-proverbs
RUN pip install -r requirements.txt

COPY . /chinese-proverbs

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]