from db.models.jobs import Job
from schemas.jobs import JobCreate
from sqlalchemy.orm import Session


def retreive_job(id: int, db: Session):
    item = db.query(Job).filter(Job.job_id == id).first()
    return item


def create_new_job(job: JobCreate, db: Session, job_owner_id: int):
    job_object = Job(**job.dict(), job_owner_id=job_owner_id)
    db.add(job_object)
    db.commit()
    db.refresh(job_object)
    return job_object


def list_jobs(db: Session):
    jobs = db.query(Job).filter(Job.job_is_active).all()
    return jobs


def update_job_by_id(id: int, job: JobCreate, db: Session, job_owner_id):
    existing_job = db.query(Job).filter(Job.job_id == id)
    if not existing_job.first():
        return 0
    job.__dict__.update(job_owner_id=job_owner_id)
    existing_job.update(job.__dict__)
    db.commit()
    return 1


def delete_job_by_id(id: int, db: Session, job_owner_id):
    existing_job = db.query(Job).filter(Job.job_id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1
