from sqlalchemy.dialects.postgresql import insert as pg_insert
from backend.database import as_session,engine
from backend.model import Job
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
import time

def timer_time(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        midle =await func(*args,**kwargs)
        end = time.perf_counter()

        print(f"function result in {end - start:.4f} seconds")
        return midle
    return wrapper


async def save_in_db(jobs: list[dict]):
    async with as_session() as s:
        for job in jobs:
            
            stmt = pg_insert(Job).values(
                title=job["title"],
                company=job.get("company", ""),
                location=job.get("location", ""),
                url=job.get("link"),
            ).on_conflict_do_nothing(index_elements=["url"])
            await s.execute(stmt)
        await s.commit()

@timer_time
async def get_remote():
    async with as_session() as s:
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        for job in jobs:
            if job.location == "Remote":
                print(f"Title:{job.title} --- {job.url}")