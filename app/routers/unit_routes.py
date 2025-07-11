from fastapi import APIRouter
from app.model.dummy_unit import DummyUnit, DummyUnitRequestSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.config.db_config import get_session

router=APIRouter(
    prefix="/unit",
    tags=["unit"],
)

@router.post("", response_model=DummyUnit, summary="Add new unit")
async def add_unit(request:DummyUnitRequestSchema,db:AsyncSession=Depends(get_session)):
    try:
        db_obj=DummyUnit.model_validate(request)
        db.add(db_obj)
        await db.commit()
        await db.close()
        return db_obj
    except Exception as e:
        await db.rollback()
        await db.close()
        raise HTTPException(status_code=500, detail=str(e))