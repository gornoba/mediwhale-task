from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class AbstractModel(Base):
    __abstract__ = True  # 테이블이 생성되지 않도록 설정
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, comment="Primary key of the table")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="생성날짜")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True, comment="수정날짜")

class HospitalModel(AbstractModel):
    __tablename__ = "hospital"

    name = Column(String, index=True)
    address = Column(String, index=True)
    department = Column(String, index=True)

    patients = relationship("PatientModel", back_populates="hospital")

class PatientModel(AbstractModel):
    __tablename__ = "patient"

    patientID = Column(String, unique=True, index=True)
    birthDate = Column(String)
    sex = Column(String)

    studies = relationship("StudyModel", back_populates="patient", cascade="all, delete-orphan", lazy="joined")
    hospital_id = Column(UUID(as_uuid=True), ForeignKey("hospital.id"))
    hospital = relationship("HospitalModel", back_populates="patients", lazy="joined")

class StudyModel(AbstractModel):
    __tablename__ = "study"

    examDate = Column(String)
    laterality = Column(String)
    aiScore = Column(Float)

    patient_id = Column(UUID(as_uuid=True), ForeignKey("patient.id"))
    patient = relationship("PatientModel", back_populates="studies")
    images = relationship("ImageModel", back_populates="study", cascade="all, delete-orphan", lazy="joined")

class ImageModel(AbstractModel):
    __tablename__ = "image"

    filename = Column(String)
    data = Column(Text)

    study_id = Column(UUID(as_uuid=True), ForeignKey("study.id"))
    study = relationship("StudyModel", back_populates="images", lazy="joined")

class UrlModel(Base):
    __tablename__ = "url"

    url = Column(String, primary_key=True, unique=True, nullable=False)