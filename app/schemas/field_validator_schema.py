from pydantic import BaseModel


class FieldValidatorSchema(BaseModel):
    field_name:str
    data_type:str
    is_field_missing:bool
    validation_description:str