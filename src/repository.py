from sqlalchemy import insert
from sqlalchemy.future import select
from src.core.database import SessionLocal
from src.model import ImageModel, PatientModel, StudyModel, UrlModel
from sqlalchemy.orm import Session

def model_to_dict(model):
  return {column.name: getattr(model, column.name) for column in model.__table__.columns}

async def getUrl(db: Session):
  findUrl = await db.execute(select(UrlModel))
  result = findUrl.scalars().first()
  result_dict = model_to_dict(result) if result else None
  return result_dict['url']

async def upsertUrl(db: Session, url: str):
  findUrl = await db.execute(select(UrlModel))
  exist_url = findUrl.scalars().first()

  if exist_url:
    exist_url.url = str(url)
  else:
    new_url = UrlModel(url=str(url))
    db.add(new_url)

  await db.commit()
  await db.refresh(exist_url or new_url)
  return exist_url or new_url

async def insertData(db: Session, patientID: str, birthDate: str, sex: str, examDate: str, laterality: str, findName: str, aiscore: float, data: str):
  findPatient = await db.execute(select(PatientModel).where(PatientModel.patientID == patientID))
  existing_patient = findPatient.scalars().first()

  new_patient = None
  if not existing_patient:
    new_patient = PatientModel(patientID=patientID, birthDate=birthDate, sex=sex)
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
  else:
    new_patient = existing_patient
  
  new_study = StudyModel(examDate=examDate, laterality=laterality, aiScore=aiscore, patient_id=new_patient.id)
  db.add(new_study)
  await db.commit()
  await db.refresh(new_study)

  new_image = ImageModel(filename=findName, data=data, study_id=new_study.id)
  db.add(new_image)
  await db.commit()
  await db.refresh(new_image)