from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.security import get_current_user_from_token
from db.models.users import User
from db.operations.jobs import (
    create_new_job,
    delete_job_by_id,
    list_jobs,
    retreive_job,
    update_job_by_id,
)
from db.session import get_db
from schemas.jobs import JobCreate, ShowJob

job_router = APIRouter()


@job_router.post(
    "/create/",
    summary="Create job",
    response_model=ShowJob,
    description="Allows authorized users to create new job listings. Provide the job title, company name, location, and description.\
          The creation date is automatically set to the current date. This endpoint requires authentication.",
)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Internal API Documentation:
    - Endpoint: POST /create/
    - Purpose: Create a new job listing in the database.
    - Auth Required: Yes, a valid JWT token must be provided to identify the current user.
    - Input: `JobCreate` model with mandatory fields for title, company, location, and description.
    - Output: `ShowJob` model including the job details with the `job_date_posted` field automatically set to the current date.
    - Error Handling: Implement error handling for unauthorized access, invalid model inputs, and database operation failures.

    Note: This function interacts with the database to create a new job record. Ensure proper session management and error handling for a seamless operation.
    """
    user_id = current_user.id
    job = create_new_job(job=job, db=db, job_owner_id=user_id)
    return job


@job_router.get(
    "/get/{id}/",
    summary="Get job",
    response_model=ShowJob,
    description="Retrieves the details of a job by its unique identifier (ID).\
          This action requires no authentication and is available to all users.",
)
def read_job(id: int, db: Session = Depends(get_db)):
    """
    Internal API Documentation:
    - **Endpoint**: GET /get/{id}/
    - **Purpose**: Retrieve a specific job from the database using its ID.
    - **Auth Required**: No.
    - **Input**: Job ID as path parameter.
    - **Output**: `ShowJob` model instance of the job.

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


@job_router.get(
    "/all/",
    summary="Get all jobs",
    response_model=List[ShowJob],
    description="Fetches a list of all job listings. \
        This endpoint does not require authentication\
              and is open to all users.",
)
def read_jobs(db: Session = Depends(get_db)):
    """
    Internal API Documentation:
    - Endpoint: GET /all/
    - Purpose: Retrieve all job listings from the database.
    - Auth Required: No.
    - Output: A list of `ShowJob` model instances.

    This function queries the database for all job records and returns them.
    """
    jobs = list_jobs(db=db)
    return jobs


@job_router.put(
    "/update/{id}/",
    summary="Update job",
    description="Updates an existing job listing with new details. This endpoint requires the user to be authenticated and authorized to update the job listing.",
)
def update_job(
    id: int,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Internal API Documentation:
    - Endpoint: PUT /update/{id}/
    - Purpose: Update a specific job listing in the database.
    - Auth Required: Yes, requires authentication and ownership or superuser status.
    - Input: Job ID as path parameter and `JobCreate` model with new job details.
    - Output: Confirmation message of successful update.

    Checks for the existence of the job, verifies ownership or superuser status, then updates the job in the database.
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


@job_router.delete(
    "/delete/{id}/",
    summary="Delete job",
    description="Deletes a job listing by its ID. This action requires the user to be either the owner of the job listing or a superuser.",
)
def delete_job(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Internal API Documentation:
    - Endpoint: DELETE /delete/{id}/
    - Purpose: Remove a specific job listing from the database.
    - Auth Required: Yes, requires ownership or superuser status.
    - Input: Job ID as path parameter.

    Verifies job existence and ownership/superuser status before deleting the job from the database.
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
