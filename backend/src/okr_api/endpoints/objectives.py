from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db_session
from ..models2 import Objective
from pydantic import BaseModel
import typing as t

router = APIRouter()

class ObjectiveCreate(BaseModel):
    """Encapsulates data for creating an Objective.

    Args:
        name (str): Name of the objective.
        description (str): Description of the objective.
    """
    name: str
    description: str

@router.post("/objectives")
async def create_objective(
    objective: ObjectiveCreate, db: Session = Depends(get_db_session)
) -> t.Dict[str, t.Any]:
    """Create a new objective."""
    new_objective = Objective(name=objective.name, description=objective.description)
    db.add(new_objective)
    db.commit()
    db.refresh(new_objective)
    return {
        "id": new_objective.id,
        "name": new_objective.name,
        "description": new_objective.description,
        "progress": new_objective.progress,
    }

@router.get("/objectives/")
async def read_objectives(
    db: Session = Depends(get_db_session)
) -> t.List[t.Dict[str, t.Any]]:
    """Retrieve all objectives."""
    objectives = db.query(Objective).all()
    return [
        {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "progress": obj.progress,
        }
        for obj in objectives
    ]

@router.get("/objectives/{objective_id}")
async def read_objective(
    objective_id: int, db: Session = Depends(get_db_session)
) -> t.Dict[str, t.Any]:
    """Retrieve an objective by ID."""
    objective = db.query(Objective).filter(Objective.id == objective_id).first()
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")
    return {
        "id": objective.id,
        "name": objective.name,
        "description": objective.description,
        "progress": objective.progress,
    }

@router.delete("/objectives/{objective_id}")
async def delete_objective(
    objective_id: int, db: Session = Depends(get_db_session)
) -> t.Dict[str, str]:
    """Delete an objective by ID."""
    objective = db.query(Objective).filter(Objective.id == objective_id).first()
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")
    db.delete(objective)
    db.commit()
    return {"message": f"Objective {objective_id} deleted successfully"}

@router.get("/objectives/{objective_id}/progress")
async def calculate_progress(
    objective_id: int, db: Session = Depends(get_db_session)
) -> t.Dict[str, t.Any]:
    """Calculate and retrieve the progress of an objective."""
    objective = db.query(Objective).filter(Objective.id == objective_id).first()
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")
    return {"id": objective.id, "progress": objective.progress}
