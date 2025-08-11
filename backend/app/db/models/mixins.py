from sqlalchemy.orm import selectinload


class Mixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     
     @classmethod
     def returning(cls):
          return None
     
     @classmethod
     def order_by(cls):
          return None
     
     @classmethod
     def selectinload(cls):
          return ()
     


class UsersMixin(Mixin):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.uuid
     
     
     
     
class SkinsMixin(Mixin):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.name
     
     @classmethod
     def order_by(cls):
          return cls.name
     
     
     
     

class SkinsPriceInfoMixin(Mixin):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.skin_name
     
     
     
class SkinsPriceHistoryMixin(Mixin):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.timestamp
     
     
     
class UsersSkinsMixin(Mixin):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod 
     def selectinload(cls):
          return (selectinload(cls.skin), selectinload(cls.user))
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.skin_name
     
     
class UsersNotifyMixin(Mixin):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
          
     @classmethod
     def order_by(cls):
          return cls.uuid
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def selectinload(cls):
          return (selectinload(cls.user),)
     
     

     
     
          
     