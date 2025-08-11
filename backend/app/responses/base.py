from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from slowapi.errors import RateLimitExceeded

from .abstract import AbstractResponse



class BaseResponse(AbstractResponse):
     description = ""
     detail = ""
     status_code = 200
          
     
     @classmethod
     def response(cls) -> JSONResponse:
          return JSONResponse(
               content={"detail": cls.detail},
               status_code=cls.status_code
          )
          
     @classmethod
     def exec(cls) -> HTTPException:
          return HTTPException(
               status_code=cls.status_code,
               detail=cls.detail
          )
          
     @classmethod
     def schema(cls) -> dict[int, dict]:
          return {
               cls.status_code: {
                    "description": cls.description,
                    "content": {
                         "application/json": {
                              "example": {
                                   cls.__name__: {"detail": cls.detail}
                              }
                         }
                    }
               }
          }  
          
     @classmethod
     def dublicate(cls) -> dict[str, dict[str, str]]:
          return {cls.__name__: {"detail": cls.__name__}}   
     
          
     
def isresponse(obj: type) -> bool:
     return isinstance(obj, type) and AbstractResponse in obj.mro()




def router_responses(*values: AbstractResponse) -> dict[int, dict]:
     responses = {}
     for resp in values:
          schema = resp.schema()
          if resp.status_code in responses.keys():
               (
                    responses[resp.status_code]
                    ["content"]
                    ["application/json"]
                    ["example"]
                    .update(resp.dublicate())
               )
          responses.update(schema)
     return responses


