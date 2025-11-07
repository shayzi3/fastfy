from fastapi.responses import JSONResponse
from fastapi import HTTPException

from .abc import BaseResponse



class Response(BaseResponse):
     description = "Empty"
     status_code = 200
          
          
     @classmethod
     def response(cls) -> JSONResponse:
          return JSONResponse(
               content={"detail": cls.description},
               status_code=cls.status_code
          )
          
     @classmethod
     def exec(cls) -> HTTPException:
          return HTTPException(
               status_code=cls.status_code,
               detail=cls.description
          )
          
     @classmethod
     def schema(cls) -> dict[int, dict]:
          return {cls.status_code: {"description": cls.description}}
     
          
     
def isresponse(obj: type) -> bool:
     return isinstance(obj, type) and BaseResponse in obj.mro()


def router_responses(*values: BaseResponse) -> dict[int, dict[str, str]]:
     responses = {}
     for resp in values:
          schema = resp.schema()
          if resp.status_code in responses.keys():
               responses[resp.status_code]["description"] += f" | {schema[resp.status_code]['description']}"
          else:
               responses.update(schema)
     return responses


