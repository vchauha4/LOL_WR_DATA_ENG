from dataclasses import dataclass, field
from typing import List, Dict
from userEntity import User
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("API_KEY")

@dataclass
class MatchRecord:
    match_id: str
    # championName: str
    # winloss: str
    winlossChamp: dict= field(default_factory=dict)

    user : User
    matches: list= field(default_factory=list)

    def getMatches(self, type=None):
        if type:

            resp= requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.user.puuid}/ids?type={type}&start=0&count={100}&api_key='+API_KEY)
            self.matches= resp.json()
        else:
            resp= requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.user.puuid}/ids?start=0&count={100}&api_key='+API_KEY)
            self.matches= resp.json()
    
    def getMatchId(self):
        for match in self.matches:
            resp= requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}?api_key='+API_KEY)
            jsonResp= resp.json()

            champ=jsonResp['Champ']# Need to get actual value
            isWin=bool(jsonResp['Result'])# Need to get actual value

            if champ not in self.winlossChamp:
                self.winlossChamp[champ] = {'Win': 0, 'Loss': 0}

                if isWin:
                    self.winlossChamp[champ]['Win'] += 1
                else:
                    self.winlossChamp[champ]['Loss'] += 1


         

