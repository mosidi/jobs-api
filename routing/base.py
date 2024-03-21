from fastapi import APIRouter

from . import route_jobs, route_login, route_users

api_router = APIRouter()

api_router.include_router(route_users.users_router, prefix="/users", tags=["users"])
api_router.include_router(route_jobs.job_router, prefix="/jobs", tags=["jobs"])
api_router.include_router(route_login.login_router, prefix="/login", tags=["login"])


@api_router.get("/")
async def read_main():
    """
    Retrieves the main endpoint of the API.

    Returns:
        dict: A dictionary containing the message "Hello World".
    """
    return {"msg": "Hello World"}
