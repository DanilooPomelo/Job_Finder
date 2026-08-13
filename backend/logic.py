import selectors

from sqlalchemy.dialects.postgresql import insert as pg_insert
from backend.database import as_session,engine
from backend.model import Job
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
import time
import asyncio
loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
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

def arbeitnow_adaptor(jobs):
    arbeit = []
    for job in jobs:
        arbe = {
           "source": "ARBEITNOW",
            "title": job["title"],
            "company":job["company_name"],
            "location":job["remote"],
            "url":job["url"],
            "snippet":job["description"],
            "updated":job["created_at"] 
        }
        arbeit.append(arbe)
    asyncio.run(save_in_db(arbeit), loop_factory=loop)


def adzuna_adaptor(jobs):
    adzuna = []
    for job in jobs:
        adzunaj = {
            "source": "ADZUNA",
            "title": job["title"],
            "company":job["company"]["display_name"],
            "location":job["location"]["display_name"],
            "url":job["redirect_url"],
            "snippet":job["description"],
            "updated":job["created"]
        }
        adzuna.append(adzunaj)
    asyncio.run(save_in_db(adzuna), loop_factory=loop)
    
def jooble_adaptor(jobs):
    joobler = []
    for job in jobs:
        jobles = {
                    "source": "JOOBLE",
                    "title": job['title'],
                    "company": job.get("company", ""),
                    "location":job.get("location", ""),
                    "url": job.get("link"),
                    "snippet":job.get("snippet", ""),
                    "updated": job.get("updated", "")
        
                }
        joobler.append(jobles)
    asyncio.run(save_in_db(joobler), loop_factory=loop)
    for job in joobler:
        print(job['title'],"---" , job['updated'])
    
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
    