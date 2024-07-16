from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.model import  PatientModel

async def getAllPatient(db: Session, skip: int, limit: int):
  result = await db.execute(select(PatientModel))
  return result.scalars().unique()

async def getPatient(db: Session, id: str):
  result = await db.execute(select(PatientModel).where(PatientModel.id == id))
  return result.scalars().first()

