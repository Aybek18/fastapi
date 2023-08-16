from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.config import settings
from base_class import Base
from core.exceptions import EventAppBaseException
from core.routers import api_router
from core.session import engine
from core.utils import pascal_case


def include_router(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, debug=settings.DEBUG)
    create_tables()
    include_router(app)

    return app


app = start_application()


@app.exception_handler(EventAppBaseException)
async def base_exception_handler(request: Request, exc: EventAppBaseException):
    return JSONResponse(
        status_code=exc.http_code,
        content={"code": exc.code, "message": exc.message},
    )


@app.exception_handler(HTTPException)
async def base_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": pascal_case(exc.detail), "message": exc.detail},
    )
