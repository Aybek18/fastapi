from starlette import status


class EventAppBaseException(Exception):
    code = "UnexpectedException"
    message = "Unexpected error occurred while processing your request"
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, code: str = None, message: str = None, http_code: int = None):
        self.code = code or self.code
        self.message = message or self.message
        self.http_code = http_code or self.http_code


class EventAppBadRequest(EventAppBaseException):
    code = "BadRequest"
    message = "Bad Request"
    http_code = status.HTTP_400_BAD_REQUEST


class FirebaseError(EventAppBadRequest):
    code = "InvalidToken"
    message = "Invalid token"


class EventAppNotFound(EventAppBaseException):
    code = "NotFound"
    message = "Not found"
    http_code = status.HTTP_404_NOT_FOUND


class EventAppUserNotFound(EventAppNotFound):
    code = "UserDoesNotExists"
    message = "User does not exists"


class EventAppUserAlreadyExists(EventAppBaseException):
    code = "UserAlreadyExists"
    message = "User already exists"
    http_code = status.HTTP_409_CONFLICT


class EventAppUnauthorized(EventAppBaseException):
    code = "UnauthorizedOrInvalidCredentials"
    message = "Unauthorized or invalid credentials"
    http_code = status.HTTP_401_UNAUTHORIZED


class EventAppUserNotActive(EventAppUnauthorized):
    code = "UserIsNotActive"
    message = "User is not active"


class EventAppInvalidToken(FirebaseError):
    http_code = status.HTTP_401_UNAUTHORIZED
