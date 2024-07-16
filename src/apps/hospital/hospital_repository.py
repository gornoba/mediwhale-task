from datetime import datetime
from http.client import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.apps.hospital import hospital_schema
from src.models.model import HospitalModel, PatientModel

async def getAllHospital(db: Session):
  result = await db.execute(select(HospitalModel))
  return result.scalars().all()

async def getHospital(db: Session, id: str):
  result = await db.execute(select(HospitalModel).where(HospitalModel.id == id))
  return result.scalars().first()

async def createHospital(db: Session, body: hospital_schema.HospitalModelSchema):
  result = HospitalModel(
    name=body.name,
    address=body.address if hasattr(body, 'address') else None,
    department=body.department if hasattr(body, 'department') else None
  )
  
  db.add(result)
  await db.commit()
  await db.refresh(result)
  return result

async def updateHospital(db: Session, id: str, body: hospital_schema.HospitalModelSchema):
  findHospital = await getHospital(db, id)
  
  if not findHospital:
    return HTTPException(status_code=404, detail="Hospital not found")
  
  findHospital.name = body.name
  findHospital.address = body.address if hasattr(body, 'address') else None
  findHospital.department = body.department if hasattr(body, 'department') else None
  findHospital.updated_at = datetime.now()

  await db.commit()
  await db.refresh(findHospital)
  return findHospital

async def deleteHospital(db: Session, id: str):
  findHospital = await getHospital(db, id)
  
  if not findHospital:
    return HTTPException(status_code=404, detail="Hospital not found")
  
  await db.delete(findHospital)
  await db.commit()

async def hospitalPatient(db: Session, hospital_id: str, patient_id: str):
  findPaient = await db.execute(select(PatientModel).where(PatientModel.id == patient_id))
  findPaient = findPaient.scalars().first()

  if not findPaient:
    return HTTPException(status_code=404, detail="Patient not found")

  findHospital = await getHospital(db, hospital_id)

  if not findHospital:
    return HTTPException(status_code=404, detail="Hospital not found")
  
  findPaient.hospital_id = hospital_id

  await db.commit()
  await db.refresh(findPaient)

  return findPaient