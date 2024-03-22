import os

from fastapi import FastAPI
from mangum import Mangum

from core.config import settings
from db.base import Base
from db.session import engine
from routing.base import api_router


def include_router(app):
    app.include_router(api_router, prefix="/v1")


def create_tables():
    """
    Create database tables.
    """
    print("create database tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    """
    Creates and configures a FastAPI application.

    Returns:
        app (FastAPI): The configured FastAPI application.
    """
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    create_tables()
    return app


app = start_application()
if "LAMBDA_PRODUCTION" in os.environ and os.environ["LAMBDA_PRODUCTION"] == "true":
    handler = Mangum(app)
