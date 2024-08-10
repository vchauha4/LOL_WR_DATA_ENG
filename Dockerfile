FROM python:3.9-slim

WORKDIR /Data_retrieval
COPY Data_retrieval/requirements.txt .

RUN pip install -r requirements.txt
COPY Data_retrieval/summonerIDs_to_PUUID.py .
COPY .env .env

CMD [ "python", "summonerIDs_to_PUUID.py" ]