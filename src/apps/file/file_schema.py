from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel

class ImageModelSchema(BaseModel):
    id: uuid.UUID
    filename: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class StudyModelSchema(BaseModel):
    id: uuid.UUID
    examDate: str
    laterality: str
    aiScore: float
    created_at: datetime
    updated_at: Optional[datetime]
    images: List[ImageModelSchema] = []

    class Config:
        orm_mode = True

class PatientModelSchema(BaseModel):
    id: uuid.UUID
    patientID: str
    birthDate: str
    sex: str
    created_at: datetime
    updated_at: Optional[datetime]
    studies: List[StudyModelSchema] = []

    class Config:
        orm_mode = True

class HospitalModelSchema(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    department: str
    created_at: datetime
    updated_at: Optional[datetime]
    patients: List[PatientModelSchema] = []

    class Config:
        orm_mode = True