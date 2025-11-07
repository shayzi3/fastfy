from .base import Response



class LoginSuccess(Response):
     description = "Login success"
     
     
class CreateSuccess(Response):
     description = "Data created success"
     
     
class DeleteSuccess(Response):
     description = "Data deleted success"
     

class UpdateSuccess(Response):
     description = "Data updated success"