from fastapi import APIRouter

from events.routers import event_router
from notifications.routers import notification_router
from users.routers import user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users", ])
api_router.include_router(notification_router, prefix="/notifications", tags=["notifications", ])
api_router.include_router(event_router, prefix="/events", tags=["events", ])
