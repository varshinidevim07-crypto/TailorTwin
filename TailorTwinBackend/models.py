
from pydantic import BaseModel, Field


# Customer measurement model
class Measurement(BaseModel):
    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hip: float = Field(gt=0)
    shoulder: float = Field(gt=0)
    sleeve: float = Field(gt=0)


# Garment pattern request model
class PatternRequest(BaseModel):
    garment: str

    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hip: float = Field(gt=0)

    shoulder: float = Field(gt=0)
    sleeve: float = Field(gt=0)
    armhole: float = Field(gt=0)
    neck: float = Field(gt=0)
    upper_arm: float = Field(gt=0)


# Fabric calculation request model
class FabricRequest(BaseModel):
    garment: str

    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hip: float = Field(gt=0)

    fabric_width: float = Field(default=150, gt=0)
