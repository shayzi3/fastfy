from typing import Protocol, Any

from fastapi.responses import RedirectResponse




class BaseOpenID(Protocol):
     
     
     async def redirect_user(self, url: str) -> RedirectResponse:
           ...
           
           
     async def construct_url(self, return_to: str, realm: str = "") -> str:
          ...
          
          
     async def validate_results(self, query_params: Any) -> Any:
          ...