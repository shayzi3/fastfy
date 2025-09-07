

class Singleton:
     _instanses = {}
     
     def __new__(cls, *args, **kwargs):
          if cls.__name__ not in cls._instanses.keys():
               cls._instanses[cls.__name__] = super().__new__(cls)
          return cls._instanses[cls.__name__]