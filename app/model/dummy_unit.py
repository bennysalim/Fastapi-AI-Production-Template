from sqlmodel import Field, Relationship, SQLModel
from sqlmodel import SQLModel
from typing import TYPE_CHECKING,  Optional

from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.dummy_project import DummyProject


class DummyUnitBase(SQLModel):
    dummy_project_id:str=Field(nullable=False, foreign_key="project.id")
    code: str=Field(nullable=False)
    name:str=Field(nullable=False)
    description:Optional[str]=Field(nullable=True)

    class Config:
        arbitrary_types_allowed=True
        from_attributes=True

class DummyUnitFullBase(DummyUnitBase, BaseModel):
    pass

class DummyUnit(DummyUnitFullBase, table=True):
    __tablename__="unit"
    dummy_project:'DummyProject' = Relationship(back_populates="dummy_unit", 
                                                sa_relationship_kwargs={'lazy': 'select'})
    
class DummyUnitRequestSchema(DummyUnitBase):
    pass