from typing import Any
from fastapi.responses import RedirectResponse
from pysteamsignin.steamsignin import SteamSignIn

from ..abc import BaseOpenID



class SteamOpenID(BaseOpenID):
     def __init__(self):
          self.steamsignin = SteamSignIn()
     
     
     async def redirect_user(self, url: str) -> RedirectResponse:
          return self.steamsignin.RedirectUser(strPostData=url)
     
     
     async def construct_url(self, return_to: str, realm: str = ""):
          return self.steamsignin.ConstructURL(responseURL=return_to)
     
     
     async def validate_results(self, query_params: Any) -> bool | str:
          return self.steamsignin.ValidateResults(results=query_params)