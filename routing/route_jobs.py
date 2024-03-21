from typing import List

from .route_login import get_current_user_from_token
from db.models.users import User
from db.operations.jobs import (
    create_new_job,
    delete_job_by_id,
    list_jobs,
    retreive_job,
    update_job_by_id,
)
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.jobs import JobCreate, ShowJob
from sqlalchemy.orm import Session

job_router = APIRouter()


@job_router.post("/create/", summary="Create job", response_model=ShowJob)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    A function to create a new job by the current user.
    Parameters:
        job (JobCreate): The details of the job to be created.
        db (Session): The database session.
        current_user (User): The current user creating the job.

    Returns:
        The newly created job.
    """
    user_id = current_user.id
    job = create_new_job(job=job, db=db, job_owner_id=user_id)
    return job


@job_router.get("/get/{id}/", summary="Get job", response_model=ShowJob)
def read_job(id: int, db: Session = Depends(get_db)):
    """
    Get a job by its ID.

    Parameters:
        id (int): The ID of the job to retrieve.
        db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.

    Returns:
        ShowJob: The retrieved job.

    Raises:
        HTTPException: If the job with the specified ID does not exist.
    """
    job = retreive_job(id=id, db=db)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with this id {id} does not exist",
        )
    return job


@job_router.get("/all/", summary="Get all jobs", response_model=List[ShowJob])
def read_jobs(db: Session = Depends(get_db)):
    """
    A description of the entire function, its parameters, and its return types.
    """
    jobs = list_jobs(db=db)
    return jobs


@job_router.put("/update/{id}/", summary="Update job")
def update_job(
    id: int,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Update job function to modify an existing job entry in the database.

    Parameters:
        id (int): The unique identifier of the job to be updated.
        job (JobCreate): The updated job data.
        db (Session): The database session.
        current_user (User): The current user making the update request.

    Returns:
        dict: A dictionary with a detail key indicating the success of the update operation.
    """
    job_owner_id = current_user.id
    job_retrieved = retreive_job(id=id, db=db)
    if not job_retrieved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id {id} does not exist",
        )
    if job_retrieved.job_owner_id == current_user.id or current_user.is_superuser:
        update_job_by_id(id=id, job=job, db=db, job_owner_id=job_owner_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update.",
        )
    return {"detail": "Successfully updated data."}


@job_router.delete("/delete/{id}/", summary="Delete job")
def delete_job(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Delete a job by its ID if the requesting user is the job owner or a superuser.

    Parameters:
        id (int): The ID of the job to delete.
        db (Session): The database session.
        current_user (User): The current user making the request.

    Returns:
        dict: A message indicating if the job was successfully deleted, or raises an HTTPException with a 404 or 401 status code.
    """
    job = retreive_job(id=id, db=db)
    if not job:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with {id} does not exist",
        )

    if job.job_owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id, db=db, job_owner_id=current_user.id)
        return {"msg": "Job successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted !"
    )
