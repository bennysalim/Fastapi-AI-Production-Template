from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.dummy_project import DummyProject, DummyProjectRequestSchema
from fastapi import APIRouter, Depends, HTTPException
from app.config.db_config import get_session

router=APIRouter(
    prefix="/project",
    tags=["project"],
)

@router.post("", response_model=DummyProject, summary="Add new project")
async def add_project(request:DummyProjectRequestSchema, db:AsyncSession=Depends(get_session)):
    try:
        db_obj=DummyProject.model_validate(request)
        db.add(db_obj)
        await db.commit()
        await db.close()
        return db_obj
    except Exception as e:
        await db.rollback()
        await db.close()
        raise HTTPException(status_code=500, detail=str(e))