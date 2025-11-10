from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.models.entity import Entity
from src.services.db import get_db
from src.services.auth_dep import require_auth


router = APIRouter(prefix="/entities", tags=["entities"])

def _to_entity_out(ent: Entity) -> dict:
    return {
        "id": str(ent.id),
        "name": ent.name,
        "type": ent.type,
        "confidence": ent.confidence,
        "source": ent.source,
        "source_type": ent.source_type,
        "metadata": ent.meta,
        "is_active": ent.is_active,
    }

class EntityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    type: str
    confidence: float | None = None
    source: str | None = None
    source_type: str | None = None
    meta: dict | None = Field(default=None, alias="metadata")


class EntityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    type: str | None = None
    confidence: float | None = None
    source: str | None = None
    source_type: str | None = None
    meta: dict | None = Field(default=None, alias="metadata")


class EntityOut(BaseModel):
    id: str
    name: str
    type: str
    confidence: float | None
    source: str | None
    source_type: str | None
    # Read from ORM attribute 'meta' but expose as 'metadata'
    metadata: dict | None = Field(default=None, validation_alias="meta")
    is_active: bool

    class Config:
        from_attributes = True


@router.post("", response_model=EntityOut, status_code=201)
def create_entity(
    payload: EntityCreate,
    db: Session = Depends(get_db),
    _sub: str = Depends(require_auth),
):
    ent = Entity(**payload.model_dump())
    db.add(ent)
    db.commit()
    db.refresh(ent)
    return _to_entity_out(ent)


@router.get("", response_model=List[EntityOut])
def list_entities(
    db: Session = Depends(get_db),
    _sub: str = Depends(require_auth),
    offset: int = 0,
    limit: int = 50,
):
    q = db.query(Entity).filter(Entity.is_active.is_(True)).offset(offset).limit(limit)
    items = q.all()
    return [_to_entity_out(e) for e in items]


@router.get("/{entity_id}", response_model=EntityOut)
def get_entity(entity_id: str, db: Session = Depends(get_db), _sub: str = Depends(require_auth)):
    ent = db.get(Entity, entity_id)
    if not ent or not ent.is_active:
        raise HTTPException(status_code=404, detail="Entity not found")
    return _to_entity_out(ent)


@router.put("/{entity_id}", response_model=EntityOut)
def update_entity(
    entity_id: str,
    payload: EntityUpdate,
    db: Session = Depends(get_db),
    _sub: str = Depends(require_auth),
):
    ent = db.get(Entity, entity_id)
    if not ent or not ent.is_active:
        raise HTTPException(status_code=404, detail="Entity not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(ent, k, v)
    db.commit()
    db.refresh(ent)
    return _to_entity_out(ent)


@router.delete("/{entity_id}", status_code=204)
def delete_entity(entity_id: str, db: Session = Depends(get_db), _sub: str = Depends(require_auth)):
    ent = db.get(Entity, entity_id)
    if not ent or not ent.is_active:
        return
    ent.is_active = False
    db.commit()

