import selectors

from sqlalchemy.dialects.postgresql import insert as pg_insert
from backend.database import as_session,engine
from backend.model import Job
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
import time
import asyncio



def timer_time(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        midle =await func(*args,**kwargs)
        end = time.perf_counter()

        print(f"function result in {end - start:.4f} seconds")
        return midle
    return wrapper


    
    



    

async def save_in_db(jobs):
    saved = 0
    duplicate = 0
    async with as_session() as s:
        for job in jobs:
            
            stmt = pg_insert(Job).values(
                title=job["title"],
                company=job["company"],
                location=job["location"],
                url=job["url"],
                snippet=job["snippet"],
                updated=job["updated"],
                source=job['source']
            ).on_conflict_do_nothing(index_elements=["url"]).returning(Job.id)
            
            result = await s.execute(stmt)
            inserted_id = result.scalar_one_or_none()
            if inserted_id is not None:
                saved+=1
            else:
                duplicate += 1
        await s.commit()
    print(f"Новых: {saved} | Дубликатов: {duplicate}")




    

    
#сделать все через список без подсказок все верно расстваить! после чего можно делать вызов через бота! 
@timer_time
async def get_remote():
    async with as_session() as s:
        remote_j = []
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        for job in jobs:
            if job.location == "Remote":
                if job.snippet is None:
                    job.snippet = ""
                
                snippet = job.snippet[:125]
                remote_j.append(f"Name: {job.title} --- Description: {snippet} ===> LINK:{job.url}")
        

            

        return (remote_j)
    