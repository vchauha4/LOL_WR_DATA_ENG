from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename='numberTrack.log', level=logging.INFO, format='%(asctime)s - %(message)s')

load_dotenv()
API_KEY=os.getenv("API_KEY") 


client= MongoClient('mongodb+srv://riot_db:57NVFHjuFZhhJPEm@cluster0.j01gpse.mongodb.net/')#mongodb+srv://riot_db:57NVFHjuFZhhJPEm@cluster0.j01gpse.mongodb.net/   
db= client['Riot_DB']

summonerIdCollection= db['Summoner_IDs']
puuidCollection=db['PUUID']



def user_info(summonerId):
    url=f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key="+API_KEY
    response=requests.get(url)

    if response.status_code != 200:
        print("ERROR with ID:",summonerId)
        logging.info("ERROR with ID:",summonerId)

    else:
        response=response.json()
    return response


def get_PUUID(skip=100):
    for summoner_data in summonerIdCollection.find().sort("summonerId",1).limit(100).skip(skip):

        summonerID=summoner_data.get("summonerId")
        response= user_info(summonerID)

        data ={
        "_id": response.get("puuid"),
        "puuid": response.get("puuid"),
        "summonerLevel": response.get("summonerLevel"),
        "summonerID": response.get("id"),
        "accountId": response.get("accountId"),
        "revisionDate": response.get("revisionDate")
        }
        
        puuidCollection.update_one(
        {'_id': data['_id']},
        {'$set': data},  
        upsert=True
        )


end_time= datetime.now()+timedelta(hours=23, minutes=40)
skip=37200

while datetime.now()<end_time:
    try:
        get_PUUID(skip)
        logging.info(f'Successfully processed skip value: {skip}, {100+skip} records have been processed')
        skip+= 100
    except Exception as e:
        logging.error(f'Error at skip value {skip}: {e}')
        break
    time.sleep(130)

logging.info(f'Program stopped at skip value: {skip}')