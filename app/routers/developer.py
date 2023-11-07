from fastapi import APIRouter, Depends, Response, HTTPException
from ..dependencies import get_db
from .. import schemas, crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/developer", response_model=schemas.Developer, tags=["Developer"])
async def create_developer_route(
    developer: schemas.DeveloperCreate, db: Session = Depends(get_db)
):
    new_developer = crud.create_developer(db, developer)
    return new_developer


@router.get("/developer/{id}", response_model=schemas.Developer, tags=["Developer"])
async def read_developer_route(id: int, db: Session = Depends(get_db)):
    developer = crud.read_developer(db, id)
    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")
    return developer


@router.get("/developers", response_model=list[schemas.Developer], tags=["Developer"])
async def read_developers_route(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    developers = crud.read_developers(db, skip, limit)
    if developers is None:
        raise HTTPException(status_code=404, detail="No developers found")
    return developers


@router.put("/developer/{id}", tags=["Developer"])
async def update_developer_route(
    id: int, developer: schemas.DeveloperUpdate, db: Session = Depends(get_db)
):
    crud.update_developer(db, id, developer)
    return Response(status_code=204)


@router.delete("/developer/{id}", tags=["Developer"])
async def delete_developer_route(id: int, db: Session = Depends(get_db)):
    crud.delete_developer(db, id)
    return Response(status_code=204)
