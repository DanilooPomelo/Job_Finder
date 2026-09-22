from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.model import Job
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.logic import get_new_vac

app = FastAPI()

@app.get("/jobs")
async def get_tj(db: Session = Depends(get_db)):
    result = await get_new_vac()
    return result

#@app.get("/newjobs")
#async def get_nj(db: Session = Depends(get_db)):
#    res = await