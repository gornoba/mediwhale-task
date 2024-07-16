from src.apps.patient import patient_repository
from sqlalchemy.orm import Session

async def getAllPatient(db: Session, skip: int, limit: int):
  result = await patient_repository.getAllPatient(db, skip, limit)
  return result

async def getPatient(db: Session, id: str):
  result = await patient_repository.getPatient(db, id)
  return result

