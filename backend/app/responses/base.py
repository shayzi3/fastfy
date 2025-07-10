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
               content={"detail": cls.detail if cls.detail else cls.__name__},
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
                                   "detail": cls.detail if cls.detail else cls.__name__
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
          if list(schema.keys())[0] in responses.keys() and resp.status_code != 200:
               raise KeyError(f"dublicate status code: {schema}")
          responses.update(schema)
     return responses



def rate_limit_exceeded(request: Request, exc: RateLimitExceeded) -> JSONResponse:
     response = JSONResponse(
          {"detail": f"RequestTimeoutError: {exc.detail}"}, 
          status_code=429
     )
     response = request.app.state.limiter._inject_headers(
          response, request.state.view_rate_limit
     )
     return response