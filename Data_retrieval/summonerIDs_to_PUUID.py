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



def user_info(summonerId, retries=3, delay=600):
    url=f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key="+API_KEY

    for attempt in range(retries):
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        else:
            logging.error(f"Attempt {attempt + 1}: ERROR with Summoner ID {summonerId}, Status Code: {response.status_code}, Response: {response}")
            time.sleep(delay)

    logging.error(f"Failed to retrieve data for Summoner ID {summonerId} after {retries} attempts")
    return None



def get_PUUID(skip=100, max_skips=10):
    for summoner_data in summonerIdCollection.find().sort("summonerId",1).limit(100).skip(skip):

        summonerID=summoner_data.get("summonerId")
        response= user_info(summonerID)
        if response:

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
            skip_count = 0 
        else:
            skip_count += 1
            logging.warning(f'Skipping update for Summoner ID: {summonerID} due to failed API call.')

        if skip_count > max_skips:
            logging.error(f"Exceeded maximum skip count of {max_skips}. Terminating program.")
            return False

    return True


end_time= datetime.now()+timedelta(hours=23, minutes=40)
skip=int(os.getenv("SKIP")) 

while datetime.now()<end_time:
    if skip >= 119500:
        logging.info(f'Skip value reached {skip}. Terminating program.')
        break
    try:
        get_PUUID(skip)
        logging.info(f'Successfully processed skip value: {skip}, {100+skip} records have been processed')
        skip+= 100

    except Exception as e:
        logging.error(f'Error at skip value {skip}: {e}')
        break
    time.sleep(130)

logging.info(f'Program stopped at skip value: {skip}')