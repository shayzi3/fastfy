from aiogram.fsm.state import State, StatesGroup



class LoginState(StatesGroup):
     code = State()
     
     
class UserPercentState(StatesGroup):
     percent = State()
     
     
class SearchState(StatesGroup):
     query = State()