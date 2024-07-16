from fastapi import APIRouter
from src.apps.basic.basic_controller import router as basic_router
from src.apps.file.file_controller import router as file_router
from src.apps.hospital.hospital_controller import router as hospital_router
from src.apps.patient.patient_controller import router as patient_router

router = APIRouter()

router.include_router(basic_router, prefix='/basic', tags=['basic'])
router.include_router(file_router, prefix='/file', tags=['file'])
router.include_router(hospital_router, prefix='/hospital', tags=['hospital'])
router.include_router(patient_router, prefix='/patient', tags=['patient'])
