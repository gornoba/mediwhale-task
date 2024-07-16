from sqlalchemy.future import select
from src.models.model import ImageModel, PatientModel, StudyModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

async def insertData(db: Session, patientID: str, birthDate: str, sex: str, examDate: str, laterality: str, findName: str, aiscore: float, data: str):
  try:
    find_patient = await db.execute(select(PatientModel).where(PatientModel.patientID == patientID))
    existing_patient = find_patient.scalars().first()
    
    if not existing_patient:
      new_patient = PatientModel(patientID=patientID, birthDate=birthDate, sex=sex)
      new_study = StudyModel(examDate=examDate, laterality=laterality, aiScore=aiscore, patient=new_patient)
      new_image = ImageModel(filename=findName, data=data, study=new_study)

      new_patient.studies.append(new_study)
      new_study.images.append(new_image)
      
      db.add(new_patient)
      await db.flush()
      await db.refresh(new_patient)
    else:
      new_study = StudyModel(examDate=examDate, laterality=laterality, aiScore=aiscore, patient=existing_patient)
      new_image = ImageModel(filename=findName, data=data, study=new_study)
      
      existing_patient.studies.append(new_study)
      new_study.images.append(new_image)
      
      db.add(new_study)
      await db.flush()
      await db.refresh(new_study)

    await db.commit()
    patient = await db.execute(select(PatientModel).where(PatientModel.patientID == patientID))
    patient = patient.scalars().first()

    return patient
            
  except SQLAlchemyError as e:
    await db.rollback()
    raise e
  
  finally:
    await db.close()
