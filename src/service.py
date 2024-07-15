import requests
import base64
import io
import json
from tempfile import NamedTemporaryFile
from fastapi.responses import FileResponse, JSONResponse
import pydicom
import matplotlib.pyplot as plt
from fastapi import HTTPException, UploadFile
from src import repository
from sqlalchemy.orm import Session

async def upsertUrl(url: str, db: Session):
    result = await repository.upsertUrl(db, url=url)
    return result

async def uploadfile(file: UploadFile, db: Session):
    contents = await file.read()
    ds = pydicom.dcmread(io.BytesIO(contents))

    aiscore = None
    data = None
    if "PixelData" in ds:
        # Matplotlib를 사용하여 이미지를 생성하고 메모리에 저장
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone)
        plt.axis('off')  # 축을 끔

        buf = io.BytesIO()
        plt.savefig(buf, format='PNG', bbox_inches='tight', pad_inches=0)
        plt.close()
        buf.seek(0)

        # 이미지를 Base64로 인코딩
        data = base64.b64encode(buf.read()).decode('utf-8')
        ai_url = await repository.getUrl(db)
        aiscore = send_base64_image(data, ai_url)
        
    patientID = ds.PatientID
    birthDate = ds.PatientBirthDate
    sex = ds.PatientSex

    examDate = ds.StudyDate
    laterality = ds.Laterality
    findName = file.filename

    await repository.insertData(db, patientID, birthDate, sex, examDate, laterality, findName, aiscore, data)

    
def send_base64_image(base64_image: str, target_url: str):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"images": base64_image})
    
    response = requests.post(target_url, headers=headers, data=payload)
    result = response.json()
    
    return result['score']