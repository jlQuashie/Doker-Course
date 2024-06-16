from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine, SessionLocal
from pydantic import BaseModel
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class ItemBase(BaseModel):
    name: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemBase, db: db_dependency):
    try:
        db_item = models.Item(**item.dict())
        db.add(db_item)
        db.commit()
        return {"message": "Item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))