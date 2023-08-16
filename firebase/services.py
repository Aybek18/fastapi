import logging

import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import UserNotFoundError

from core.exceptions import EventAppBadRequest, EventAppUserNotFound, FirebaseError

cred = credentials.Certificate("firebase_sdk.json")
firebase_admin.initialize_app(cred)

logger = logging.getLogger(__name__)


class FirebaseValidateService:
    def validate_token(self, token: str) -> str:
        try:
            decoded_token = auth.verify_id_token(token)
            firebase_user = auth.get_user(decoded_token["uid"])
            if not firebase_user.disabled:
                return firebase_user.uid
            raise ValueError("We expected enabled user")
        except (
                ValueError,
                auth.InvalidIdTokenError,
                auth.ExpiredIdTokenError,
                auth.UserDisabledError,
                auth.UserNotFoundError,
        ):
            raise FirebaseError()
        except Exception:
            logger.exception("Unexpected exception while validating token")
            raise EventAppBadRequest()

    def extract_phone_number(self, token: str) -> str:
        uid = self.validate_token(token=token)
        try:
            return auth.get_user(uid).phone_number
        except UserNotFoundError:
            raise EventAppUserNotFound()

    @classmethod
    def factory(cls) -> "FirebaseValidateService":
        return cls()
