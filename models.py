from pydantic import (
    BaseModel, 
    Field, 
    ValidationError, 
    field_validator, 
    model_validator,
    field_serializer,
    model_serializer)

from enum import Enum


class Gender(Enum):
    Male = "M"
    Female = "F"


class User(BaseModel):
    name: str = Field(examples="sam")
    age: int = Field(examples=34, ge=0)
    gender: Gender = Field(description="only supported values M or F")

    # Field validation and processing values before setting data; must return the field data
    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender(cls, v: str) -> Gender:
        if v == "M":
            return Gender.Male
        elif v == "F":
            return Gender.Female
        else:
            raise ValueError("Only supported values are M or F") # failing validation
    
    # For validation of model as a whole; must return the dictionary
    @model_validator(mode="before")
    @classmethod
    def validate_user(cls, v: dict[str, any]) -> dict[str, any]:
        if "name" not in v or "age" not in v or "gender" not in v:
            raise ValueError("name, age and gender is required")
        if v["age"] > 18 and v["gender"] == "M":
            raise ValueError("Adult male not allowed")
        return v
    
    # Logic for field serialization
    @field_serializer("gender", when_used="json")
    @classmethod
    def serialize_gender(cls, v) -> str:
        if v == Gender.Male:
            return "male"
        elif v == Gender.Female:
            return "female"
    
    # logic to use complete model as whole; if required
    @model_serializer(mode="wrap", when_used="json")
    def serialize_user(self, serializer, info):
        self.name = self.name.capitalize()
        return serializer(self)


# sample data
data = {
    "name": "sam sen",
    "age": 43,
    "gender": "F"
}

try:
    # post validation it returns data.
    user = User.model_validate(data)
    print(user)
    if user.gender == Gender.Female:
        print("female")
    elif user.gender == Gender.Male:
        print("male")

except ValidationError as e:
    print(f"schema validation error, details: {e.errors()}")

print(user.model_dump_json())
