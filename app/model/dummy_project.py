from sqlmodel import Field, Relationship,  SQLModel
from typing import TYPE_CHECKING, Optional
from app.model.base_model import BaseULIDModel

if TYPE_CHECKING:
    from app.model.dummy_unit import DummyUnit

class DummyProjectBase(SQLModel):
    code: str=Field(nullable=False)
    name:str=Field(nullable=False)
    description: Optional[str]=Field(nullable=True)

class DummyProjectFullBase(DummyProjectBase, BaseULIDModel):
    pass
 
class DummyProject(DummyProjectFullBase, table=True):
    __tablename__="project"
    dummy_unit:Optional[list["DummyUnit"]] = Relationship(back_populates="dummy_project",
                                                sa_relationship_kwargs={'lazy':'select'})

    class Config:
        from_attributes=True

class DummyProjectRequestSchema(DummyProjectBase):
    pass