import datetime
from sqlmodel import SQLModel as _SQLModel, Field
from stringcase import snakecase
from sqlalchemy.orm import declared_attr

import ulid

class SQLModel(_SQLModel):
    @declared_attr
    def __tablename__(cls):
        return snakecase(cls.__name__)
    
def generate_ulid() -> str:
    return str(ulid.ulid())

class BaseULIDModel(SQLModel):
    id:str | None = Field(
        default_factory=generate_ulid,
        primary_key=True,
        index=True,
        nullable=False,
        max_length=26
    )

class BaseModel(BaseULIDModel):
    created_by:str = Field(default="benny", nullable=False)
    updated_by:str = Field(default="benny", nullable=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)