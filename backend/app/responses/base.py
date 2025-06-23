from fastapi.responses import JSONResponse
from fastapi import HTTPException

from .abstract import AbstractResponse



class BaseResponse(AbstractResponse):
     detail = None
     status_code = None
     
     
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
     
          
          

def isresponse(obj: type) -> bool:
     return isinstance(obj, type) and AbstractResponse in obj.mro()