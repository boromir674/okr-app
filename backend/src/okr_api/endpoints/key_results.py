from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db_session
from ..models2 import KeyResult
from pydantic import BaseModel
import typing as t

router = APIRouter()


class KeyResultCreate(BaseModel):
    """Encapsulates data for creating a Key Result."""
    objective_id: int
    short_description: t.Optional[str] = None
    description: str
    progress: float = 0.0
    metric: t.Optional[str] = None
    unit: t.Optional[int] = 1

class KeyResultUpdate(BaseModel):
    """Encapsulates data for updating a Key Result."""
    progress: t.Optional[float] = None
    short_description: t.Optional[str] = None   
    description: t.Optional[str] = None
    metric: t.Optional[str] = None
    unit: t.Optional[int] = None


@router.post("/key_results")
async def create_key_result(
    key_result: KeyResultCreate, db: Session = Depends(get_db_session)
) -> t.Dict[str, t.Any]:
    """Create a new key result."""
    new_key_result = KeyResult(
        objective_id=key_result.objective_id,
        short_description=key_result.short_description,
        description=key_result.description,
        progress=key_result.progress,
        metric=key_result.metric,
        unit=key_result.unit,
    )
    db.add(new_key_result)
    db.commit()
    db.refresh(new_key_result)
    return {
        "id": new_key_result.id,
        "objective_id": new_key_result.objective_id,
        "short_description": new_key_result.short_description,
        "description": new_key_result.description,
        "progress": new_key_result.progress,
        "metric": new_key_result.metric,
        "unit": new_key_result.unit,
    }

@router.get("/key_results/")
async def read_key_results(db: Session = Depends(get_db_session)) -> t.List[t.Dict[str, t.Any]]:
    """Retrieve all key results."""
    key_results = db.query(KeyResult).all()
    return [
        {
            "id": kr.id,
            "objective_id": kr.objective_id,
            "short_description": kr.short_description,
            "description": kr.description,
            "progress": kr.progress,
            "metric": kr.metric,
            "unit": kr.unit,
        }
        for kr in sorted(key_results, key=lambda x: x.objective_id)
    ]

@router.get("/key_results/{key_result_id}")
async def read_key_result(
    key_result_id: int, db: Session = Depends(get_db_session)
) -> t.Dict[str, t.Any]:
    """Retrieve a key result by ID."""
    key_result = db.query(KeyResult).filter(KeyResult.id == key_result_id).first()
    if not key_result:
        raise HTTPException(status_code=404, detail="Key result not found")
    return {
        "id": key_result.id,
        "objective_id": key_result.objective_id,
        "short_description": key_result.short_description,
        "description": key_result.description,
        "progress": key_result.progress,
        "metric": key_result.metric,
        "unit": key_result.unit,
    }

@router.put("/key_results/{key_result_id}")
async def update_key_result(
    key_result_id: int, key_result: KeyResultUpdate, db: Session = Depends(get_db_session)
) -> t.Dict[str, t.Any]:
    """Update a key result by ID."""
    existing_key_result = db.query(KeyResult).filter(KeyResult.id == key_result_id).first()
    if not existing_key_result:
        raise HTTPException(status_code=404, detail="Key result not found")

    if key_result.progress is not None:
        existing_key_result.progress = key_result.progress
    if key_result.description is not None:
        existing_key_result.description = key_result.description
    if key_result.metric is not None:
        existing_key_result.metric = key_result.metric
    if key_result.short_description is not None:
        existing_key_result.short_description = key_result.short_description
    if key_result.unit is not None:
        existing_key_result.unit = key_result.unit

    db.commit()
    db.refresh(existing_key_result)
    return {
        "id": existing_key_result.id,
        "objective_id": existing_key_result.objective_id,
        "short_description": existing_key_result.short_description,
        "description": existing_key_result.description,
        "progress": existing_key_result.progress,
        "metric": existing_key_result.metric,
        "unit": existing_key_result.unit,
    }

@router.delete("/key_results/{key_result_id}")
async def delete_key_result(
    key_result_id: int, db: Session = Depends(get_db_session)
) -> t.Dict[str, str]:
    """Delete a key result by ID."""
    key_result = db.query(KeyResult).filter(KeyResult.id == key_result_id).first()
    if not key_result:
        raise HTTPException(status_code=404, detail="Key result not found")
    db.delete(key_result)
    db.commit()
    return {"message": f"Key result {key_result_id} deleted successfully"}
