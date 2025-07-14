from pydantic import BaseModel


class FieldValidatorSchema(BaseModel):
    field_name:str
    data_type:str
    validation_description:str