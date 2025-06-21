import aiohttp

from app.core import my_config
from app.responses.abstract import AbstractResponse
from app.responses import HttpError




class HttpSteamClient:
     def __init__(self):
          self.base_url = "https://api.steampowered.com"
          self.api_key = my_config.steam_api_key
     
     
     async def get_steam_profile(self, steamids: int) -> tuple[str, str] | AbstractResponse:
          url = (
               self.base_url + 
               "/ISteamUser/GetPlayerSummaries/v0002/" +
               f"?key={self.api_key}&steamids={steamids}"
          )
          async with aiohttp.ClientSession() as session:
               try:
                    result = await session.get(url)
                    data: dict[str, dict[str, list[dict]]] = await result.json()
               except:
                    return HttpError
               
               response = data.get("response")
               if "players" in response and response.get("players"):
                    players = response.get("players")[0]
                    return (players.get("personaname"), players.get("avatarmedium"))
               return HttpError
               
               
               
               
               
               
               