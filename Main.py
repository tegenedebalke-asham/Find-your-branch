from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas

from database import (
    SessionLocal,
    engine,
    Base
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Find Your Branch API",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {
        "message": "Find Your Branch API Running"
    }

@app.get("/branches")
def get_branches(
    db: Session = Depends(get_db)
):
    return db.query(models.Branch).all()

@app.post("/branches")
def create_branch(
    branch: schemas.BranchCreate,
    db: Session = Depends(get_db)
):
    new_branch = models.Branch(
        **branch.dict()
    )

    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    return new_branch
