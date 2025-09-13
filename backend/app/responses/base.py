from fastapi.responses import JSONResponse
from fastapi import HTTPException

from .abstract import AbstractResponse



class BaseResponse(AbstractResponse):
     description = ""
     detail = ""
     status_code = 200
          
          
     @classmethod
     def content_detail(cls) -> str:
          return cls.detail if cls.detail else cls.__name__
     
     
     @classmethod
     def response(cls) -> JSONResponse:
          return JSONResponse(
               content={"detail": cls.content_detail()},
               status_code=cls.status_code
          )
          
     @classmethod
     def exec(cls) -> HTTPException:
          return HTTPException(
               status_code=cls.status_code,
               detail=cls.content_detail()
          )
          
     @classmethod
     def schema(cls) -> dict[int, dict]:
          return {
               cls.status_code: {
                    "description": cls.description,
                    "content": {
                         "application/json": {
                              "example": {
                                   "detail": [cls.content_detail()]
                              }
                         }
                    }
               }
          }
     
          
     
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
                    ["detail"]
                    .append(resp.content_detail())
               )
          else:
               responses.update(schema)
     return responses


