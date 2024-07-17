from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY=os.getenv("API_KEY")


@dataclass(frozen=False,order=True)
class User:
    summonerName: str
    summonerTag: str
    puuid : str = None
    id: str = None
    accountId: str = None
    summonerLevel: int = None

    def __post_init__(self):
        self.getPUUID()
        self.getUserInfo()

    def getPUUID(self):
        resp=requests.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.summonerName}/{self.summonerTag}?api_key='+API_KEY)
        jsonResp= resp.json()
        self.puuid= jsonResp['puuid']
    
    def getUserInfo(self):
        resp=requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.puuid}?api_key='+API_KEY)
        jsonResp= resp.json()

        self.accountId= jsonResp['accountId']
        self.id= jsonResp['id']
        self.summonerLevel= jsonResp['summonerLevel']



user=User(summonerName="LuxxyLux",summonerTag="7857")

print(user)

