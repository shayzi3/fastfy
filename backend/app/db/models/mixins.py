from sqlalchemy.orm import selectinload

from app.schemas import (
     UserModel,
     SkinModel,
     SkinPriceInfoModel,
     SkinPriceHistoryModel,
     UserSkinRelModel,
     UserSkinModel,
     UserNotifyModel,
     UserNotifyRelModel
)



class Mixin:
     pydantic_model = None
     pydantic_rel_model = None
     
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
     pydantic_model = UserModel
     
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.uuid
     
     
     
     
class SkinsMixin(Mixin):
     pydantic_model = SkinModel
     
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.name
     
     @classmethod
     def order_by(cls):
          return cls.name
     


class SkinsPriceInfoMixin(Mixin):
     pydantic_model = SkinPriceInfoModel
     
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.skin_name
     
     @classmethod
     def order_by(cls):
          return cls.skin_name
     
     
     
class SkinsPriceHistoryMixin(Mixin):
     pydantic_model = SkinPriceHistoryModel
     
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.timestamp
     
     
     
class UsersSkinsMixin(Mixin):
     pydantic_model = UserSkinModel
     pydantic_rel_model = UserSkinRelModel
     
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
     pydantic_model = UserNotifyModel
     pydantic_rel_model = UserNotifyRelModel
     
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
     
     

     
     
          
     