from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY=os.getenv("API_KEY")


@dataclass(frozen=False,order=True)
class User:
    puuid : str = None
    id: str = None
    accountId: str = None
    summonerLevel: int = None
    

    def getPUUID(self,SummonerName,SummonerTag):
        resp=requests.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{SummonerName}/{SummonerTag}?api_key='+API_KEY)
        jsonResp= resp.json()
        self.puuid= jsonResp['puuid']
    
    def getUserInfo(self):
        resp=requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.puuid}?api_key='+API_KEY)
        jsonResp= resp.json()

        self.accountId= jsonResp['accountId']
        self.id= jsonResp['id']
        self.summonerLevel= jsonResp['summonerLevel']


user=User()

user.getPUUID("LuxxyLux","7857")
user.getUserInfo()

print(user)

# myMatches=mAthc(objectMoi)
