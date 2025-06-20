from fastapi.responses import JSONResponse

from .abstract import AbstractResponse



class BaseResponse(AbstractResponse):
     message = None
     status_code = None
     
     
     @classmethod
     def response(cls) -> JSONResponse:
          return JSONResponse(
               content={
                    "message": cls.message,
                    "status": cls.status_code
               },
               status_code=cls.status_code
          )
          
          

def isresponse(obj: type) -> bool:
     return isinstance(obj, type) and AbstractResponse in obj.mro()