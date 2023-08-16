from dataclasses import dataclass
from datetime import datetime, timedelta

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from core.exceptions import EventAppUnauthorized, EventAppUserAlreadyExists, EventAppUserNotActive, EventAppInvalidToken
from firebase.services import FirebaseValidateService
from users.models import User
from users.repositories import UserRepository
from users.schemas import UserCreate


def create_token(user_id: int, expire_minutes: int, token_type: str) -> str:
    """
    Creates access or refresh token according to 'token_type'
    """
    expire_in = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = {"user_id": user_id, "expire_in": expire_in.isoformat(), f"{token_type}": True}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str, required_keys: list[str] = None) -> dict:
    """
    Decodes and validates  access or refresh token and returns decoded data
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise JWTError
    except JWTError:
        raise EventAppInvalidToken()

    for key in required_keys or []:
        if key not in payload:
            raise EventAppInvalidToken()

    return payload


@dataclass
class TokenService:
    user_repository: UserRepository

    async def execute(self, refresh_token: str, db: Session) -> str:
        user_id = await self.validate_token(token=refresh_token, token_type="refresh")

        user = self.user_repository.factory().get_by_id(instance_id=user_id, db=db)
        if not isinstance(user, User):
            raise EventAppUnauthorized()
        return create_token(user_id=user_id, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                            token_type="access")

    async def validate_token(self, token: str, token_type: str) -> int:
        token_payload = decode_token(token=token, required_keys=[f"{token_type}"])
        expire_in = datetime.fromisoformat(token_payload["expire_in"])

        if expire_in <= datetime.utcnow():
            raise EventAppUnauthorized(message=f"{token_type.capitalize()} token expired")
        return token_payload["user_id"]

    @classmethod
    def factory(cls) -> "TokenService":
        return cls(UserRepository.factory())


@dataclass
class UserAuthService:
    user_repository: UserRepository
    firebase_validate: FirebaseValidateService
    token_service: TokenService

    async def create_user_by_firebase_token(self, user: UserCreate, db: Session()) -> User:
        parsed_user = user.dict()
        firebase_token = parsed_user.pop("firebase_token")
        existing_user = await self.validate_firebase_token(firebase_token=firebase_token, db=db)
        if existing_user:
            raise EventAppUserAlreadyExists()
        return self.user_repository.create(db=db, obj_in=user)

    async def validate_firebase_token(self, firebase_token: str, db: Session()) -> User or None:
        phone_number = self.firebase_validate.factory().extract_phone_number(token=firebase_token)
        return await self.user_repository.get_user_by_phone_number(phone_number=phone_number, db=db)

    async def validate_access_token(self, access_token: str, db: Session()) -> User:
        user_id = await self.token_service.validate_token(token=access_token, token_type="access")
        existing_user = self.user_repository.get_by_id(instance_id=user_id, db=db)

        if not isinstance(existing_user, User):
            EventAppUnauthorized()

        if not existing_user.is_active:
            raise EventAppUserNotActive()
        return existing_user

    @classmethod
    def factory(cls) -> "UserAuthService":
        return cls(UserRepository.factory(), FirebaseValidateService.factory(), TokenService.factory())
