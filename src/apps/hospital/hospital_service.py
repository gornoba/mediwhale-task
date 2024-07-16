from src.apps.hospital import hospital_repository, hospital_schema
from sqlalchemy.orm import Session

async def getAllHospital(db: Session):
  result = await hospital_repository.getAllHospital(db)
  return result

async def getHospital(db: Session, id: str):
  result = await hospital_repository.getHospital(db, id)
  return result

async def createHospital(db: Session, body: hospital_schema.HospitalModelSchema):
  result = await hospital_repository.createHospital(db, body)
  return result

async def updateHospital(db: Session, id: str, body: hospital_schema.HospitalModelSchema):
  result = await hospital_repository.updateHospital(db, id, body)
  return result

async def deleteHospital(db: Session, id: str):
  await hospital_repository.deleteHospital(db, id)

async def hospitalPatient(db: Session, hospital_id: str, patient_id: str):
  result = await hospital_repository.hospitalPatient(db, hospital_id, patient_id)
  return result