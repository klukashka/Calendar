from typing import Optional
from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    email: str
    nickname: str
    password: str
    is_active: Optional[bool] = True # what's the use of None (Optional) for this field?
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    nickname: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': str(self.email),
            'nickname': str(self.nickname),
            'is_active': str(self.is_active),
            'is_superuser': str(self.is_superuser),
            'is_verified': str(self.is_verified),
        }

    class Config:
        from_attributes = True
