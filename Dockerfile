FROM python:3.9-slim

WORKDIR /Riot_Api_Source
COPY Riot_Api_Source/requirements.txt .

RUN pip install -r requirements.txt
COPY Riot_Api_Source/ .
COPY .env .env

CMD [ "python", "matchRecord.py" ]
