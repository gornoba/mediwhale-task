from http.client import HTTPException
from sqlalchemy.future import select
from src.models.model import UrlModel
from sqlalchemy.orm import Session

def model_to_dict(model):
  return {column.name: getattr(model, column.name) for column in model.__table__.columns}

async def getUrl(db: Session):
  findUrl = await db.execute(select(UrlModel))
  result = findUrl.scalars().first()

  if not result:
    raise HTTPException(status_code=404, detail="Url not found")

  return str(result.url)

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