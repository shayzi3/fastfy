from fastapi.responses import JSONResponse

from .abstract import AbstractResponse



class BaseResponse(AbstractResponse):
     description = None
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
          
          
     @classmethod
     def endpoint_response(cls) -> dict:
          return {
               "description": cls.description,
               "content": {
                    "application/json": {
                         "example": {
                              "message": cls.message,
                              "status": cls.status_code
                         }
                    }
               }
          }
     
          
          

def isresponse(obj: type) -> bool:
     return isinstance(obj, type) and AbstractResponse in obj.mro()