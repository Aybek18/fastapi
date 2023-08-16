from fastapi import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from fastapi import Depends

from core.config import settings
from core.exceptions import EventAppBadRequest
from core.session import get_db
from users.models import User
from users.repositories import UserRepository
from users.schemas import UserCreate, UserRetrieve, Token, UserRetrieveWithToken, UserRegistrationStatus, UserUpdate
from users.services import TokenService, create_token, UserAuthService

user_router = APIRouter()

security_scheme = HTTPBearer(description="Input only `Token`", )


async def get_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
                    db: Session = Depends(get_db)):
    """
    Checks token in headers and returns user
    """
    if getattr(credentials, "scheme") != "Bearer":
        raise EventAppBadRequest(message="Invalid authentication scheme")
    user = await UserAuthService.factory().validate_access_token(access_token=credentials.credentials, db=db)
    return user


@user_router.post("/me/", response_model=UserRetrieveWithToken)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    API for user creation
    """
    user = await UserAuthService.factory().create_user_by_firebase_token(user=user, db=db)

    access_token = create_token(user_id=user.id, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                                token_type="access")
    refresh_token = create_token(user_id=user.id, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES, token_type="refresh")
    user.access_token = access_token
    user.refresh_token = refresh_token
    return user


@user_router.get("/me/", response_model=UserRetrieve)
async def get_user(user: User = Depends(get_token)):
    """
    API returns user profile info
    """
    return user


@user_router.patch("/me/", response_model=UserRetrieve)
async def update_user(update_data: UserUpdate, user: User = Depends(get_token), db: Session() = Depends(get_db)):
    """
    API for updating user profile
    """
    user = UserRepository.factory().update(db=db, db_obj=user, obj_in=update_data)
    return user


@user_router.post("/login/", response_model=UserRetrieveWithToken)
async def user_login(firebase_token: str, db: Session = Depends(get_db)):
    """
    API for login with firebase token
    """
    user = await UserAuthService.factory().validate_firebase_token(firebase_token=firebase_token, db=db)
    access_token = create_token(user_id=user.id, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                                token_type="access")
    refresh_token = create_token(user_id=user.id, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES, token_type="refresh")
    user.access_token = access_token
    user.refresh_token = refresh_token
    return user


@user_router.post("/refresh-access-token/", response_model=Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    API for refreshing access_token
    """
    access_token = await TokenService.factory().execute(refresh_token=refresh_token, db=db)

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/check-registration-status/", response_model=UserRegistrationStatus)
async def check_registration_status(phone_number: str, db: Session = Depends(get_db)):
    """
    API checks for user registration status
    """
    user = await UserRepository.factory().get_user_by_phone_number(phone_number=phone_number, db=db)
    return {"is_registered": bool(user)}
