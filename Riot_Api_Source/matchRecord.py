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
    user : User
    winlossChamp: dict= field(default_factory=dict)
    win_rate_champ: dict= field(default_factory=dict)
    matches: list= field(default_factory=list)

    def __post_init__(self):
        print(f"Retrieving Win Rate per Champion for {user.summonerName}#{user.summonerTag}:")
        self.getMatches()
        self.getMatchId()     
      
        print(self.winlossChamp)


    def getMatches(self, type=None, num_games=92):
        if type:
            resp= requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.user.puuid}/ids?type={type}&start=0&count={num_games}&api_key='+API_KEY)
            self.matches= resp.json()
        else:
            resp= requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.user.puuid}/ids?start=0&count={num_games}&api_key='+API_KEY)
            self.matches= resp.json()
    
    def getMatchId(self):
        for match in self.matches:
            resp= requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}?api_key='+API_KEY)
            jsonResp= resp.json()

            participants=jsonResp['metadata']['participants']
            participantNum=participants.index(self.user.puuid)

            champ=jsonResp['info']['participants'][participantNum]['championName']
            isWin=bool(jsonResp['info']['participants'][participantNum]['win'])

            if champ not in self.winlossChamp:
                self.winlossChamp[champ] = {'Win': 0, 'Loss': 0}

            if isWin:
                self.winlossChamp[champ]['Win'] += 1
            else:
                self.winlossChamp[champ]['Loss'] += 1

    

user=User(summonerName="LuxxyLux",summonerTag="7857")
match=MatchRecord(user=user)


"""
User(puuid='oK4FypbTjZ17egkE007Xr3t429vd5f081thYY7PjIJAh5NvuX1DqiPCG2Pi2cYxxrSSCT7VNJkmo8Q', id='BkSjHMop17nMFgByrq1RnZDWrBXiEZDOFEB72fELUQO0pJGXfw2rSjP79w', accountId='lIBnjb5mx54u46e7kXv3cseHGMwzVAkZ6pO7bqcQTl4i95l-_fS15roA', summonerLevel=396)
MatchRecord(user=User(puuid='oK4FypbTjZ17egkE007Xr3t429vd5f081thYY7PjIJAh5NvuX1DqiPCG2Pi2cYxxrSSCT7VNJkmo8Q', id='BkSjHMop17nMFgByrq1RnZDWrBXiEZDOFEB72fELUQO0pJGXfw2rSjP79w', accountId='lIBnjb5mx54u46e7kXv3cseHGMwzVAkZ6pO7bqcQTl4i95l-_fS15roA', summonerLevel=396), 

winlossChamp={'Pyke': {'Win': 5, 'Loss': 3}, 'Lux': {'Win': 11, 'Loss': 14}, 'Ahri': {'Win': 1, 'Loss': 1}, 'Xayah': {'Win': 2, 'Loss': 2}, 'Vex': {'Win': 0, 'Loss': 3}, 'Ekko': {'Win': 1, 'Loss': 0}, 'Neeko': {'Win': 3, 'Loss': 1}, 'Blitzcrank': {'Win': 0, 'Loss': 2}, 'Morgana': {'Win': 2, 'Loss': 1}, 'Vi': {'Win': 1, 'Loss': 1}, 'Karma': {'Win': 3, 'Loss': 1}, 'Nunu': {'Win': 0, 'Loss': 2}, 'Alistar': {'Win': 3, 'Loss': 0}, 'Kayn': {'Win': 0, 'Loss': 1}, 'Janna': {'Win': 1, 'Loss': 1}, 'Bard': {'Win': 1, 'Loss': 0}, 'Caitlyn': {'Win': 1, 'Loss': 1}, 'Zoe': {'Win': 0, 'Loss': 1}, 'Syndra': {'Win': 1, 'Loss': 1}, 'Evelynn': {'Win': 2, 'Loss': 1}, 'Orianna': {'Win': 1, 'Loss': 0}, 'Velkoz': {'Win': 0, 'Loss': 2}, 'Briar': {'Win': 1, 'Loss': 0}, 'Nocturne': {'Win': 0, 'Loss': 1}, 'LeeSin': {'Win': 1, 'Loss': 0}, 'Malzahar': {'Win': 0, 'Loss': 2}, 'Zyra': {'Win': 0, 'Loss': 2}, 'Kayle': {'Win': 0, 'Loss': 1}, 'Gwen': {'Win': 1, 'Loss': 0}, 'Akali': {'Win': 0, 'Loss': 1}, 'Sona': {'Win': 0, 'Loss': 1}, 'Irelia': {'Win': 0, 'Loss': 1}, 'Jhin': {'Win': 1, 'Loss': 0}, 'Galio': {'Win': 1, 'Loss': 0}}, 
win_rate_champ={'Pyke': 62.5, 'Lux': 44.0, 'Ahri': 50.0, 'Xayah': 50.0, 'Vex': 0.0, 'Ekko': 100.0, 'Neeko': 75.0, 'Blitzcrank': 0.0, 'Morgana': 66.67, 'Vi': 50.0, 'Karma': 75.0, 'Nunu': 0.0, 'Alistar': 100.0, 'Kayn': 0.0, 'Janna': 50.0, 'Bard': 100.0, 'Caitlyn': 50.0, 'Zoe': 0.0, 'Syndra': 50.0, 'Evelynn': 66.67, 'Orianna': 100.0, 'Velkoz': 0.0, 'Briar': 100.0, 'Nocturne': 0.0, 'LeeSin': 100.0, 'Malzahar': 0.0, 'Zyra': 0.0, 'Kayle': 0.0, 'Gwen': 100.0, 'Akali': 0.0, 'Sona': 0.0, 'Irelia': 0.0, 'Jhin': 100.0, 'Galio': 100.0}, 

matches=['NA1_5041255982', 'NA1_5040810516', 'NA1_5040803560', 'NA1_5040527712', 'NA1_5040494883', 'NA1_5039986986', 'NA1_5038985507', 'NA1_5038978344', 'NA1_5038974185', 'NA1_5038651704', 'NA1_5038334074', 'NA1_5038326787', 'NA1_5037946344', 'NA1_5037935378', 'NA1_5037823702', 'NA1_5037815179', 'NA1_5037806228', 'NA1_5037468344', 'NA1_5037455335', 'NA1_5037339510', 'NA1_5036686818', 'NA1_5036667676', 'NA1_5036646030', 'NA1_5036489770', 'NA1_5036479573', 'NA1_5036183765', 'NA1_5036167177', 'NA1_5036148687', 'NA1_5035636718', 'NA1_5035627282', 'NA1_5035483048', 'NA1_5035463624', 'NA1_5035457979', 'NA1_5035098815', 'NA1_5035077931', 'NA1_5034668490', 'NA1_5034669770', 'NA1_5034462310', 'NA1_5034066135', 'NA1_5034053616', 'NA1_5034030796', 'NA1_5034026238', 'NA1_5033665619', 'NA1_5033620047', 'NA1_5033394996', 'NA1_5033390774', 'NA1_5033134466', 'NA1_5033120830', 'NA1_5033102183', 'NA1_5033023538', 'NA1_5032813504', 'NA1_5032430691', 'NA1_5032420141', 'NA1_5031855982', 'NA1_5031767119', 'NA1_5031666051', 'NA1_5030455589', 'NA1_5030296586', 'NA1_5029985101', 'NA1_5029920718', 'NA1_5029916820', 'NA1_5016617367', 'NA1_5016477832', 'NA1_5016225295', 'NA1_5015991174', 'NA1_5015934114', 'NA1_5015870593', 'NA1_5015832883', 'NA1_5015816069', 'NA1_5015698970', 'NA1_5015523248', 'NA1_5015121200', 'NA1_5014256354', 'NA1_5014215791', 'NA1_5014203959', 'NA1_5013907063', 'NA1_5013704338', 'NA1_5013646984', 'NA1_5013605342', 'NA1_5013595255', 'NA1_5013520022', 'NA1_5013462559', 'NA1_5013015982', 'NA1_5012980789', 'NA1_5012517383', 'NA1_5012414535', 'NA1_5012359997', 'NA1_5012340102', 'NA1_5012243290', 'NA1_5011590089', 'NA1_5011386288', 'NA1_5011378343'])
"""