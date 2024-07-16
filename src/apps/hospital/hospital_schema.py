from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HospitalPostSchema(BaseModel):
    name: str = Field(..., example="병원이름")
    address: Optional[str] = Field(None, example="주소(선택값)")
    department: Optional[str] = Field(None, example="부서(선택값)")

class HospitalModelSchema(HospitalPostSchema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True